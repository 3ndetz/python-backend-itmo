from fastapi import FastAPI, Response, WebSocket, HTTPException, status, Query, APIRouter
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel
from http import HTTPStatus
import uuid
import random


app = FastAPI(title="My Shop Server")

# Data storage (in-memory for simplicity)
carts = {}
items = {}

# Models


class Item(BaseModel):
    id: int
    name: str
    price: float
    deleted: bool = False


class CartItem(BaseModel):
    id: int
    name: str
    quantity: int
    available: bool


class Cart(BaseModel):
    id: int
    items: List[CartItem] = []
    price: float
    quantity: int


#cart = APIRouter(prefix='/cart')

print("====== = == = =========== running app test =============== = == = ")

### Cart endpoints
##@cart.post("/gdg", status_code=HTTPStatus.CREATED)
##async def create_cart(response: Response):
##    lfodsg()
##    lfodsg()
##    lfodsg()
##    lfodsg()
##    cart_id = len(carts) + 1
##    carts[cart_id] = Cart(id=cart_id, items=[], price=0)
##    response.headers['location'] = f'/cart/{cart_id}'
##    print("created cart", cart_id)
##    return response
##
    
#app.include_router(cart)

@app.post(
    "/cart",
    status_code=status.HTTP_201_CREATED
)
def create_cart(response: Response):
    cart_id = len(carts.keys()) + 1
    cartt = Cart(id=cart_id, items=[], price=0.0, quantity=0)
    carts[cart_id] = cartt
    response.headers['location'] = f'/cart/{cart_id}'
    return {"id": cart_id}


@app.get("/cart/{id}")
def get_cart(id: int) -> Cart:
    if id not in carts:
        raise HTTPException(status_code=404, detail="Cart not found")
    return carts[id]


@app.get("/cart")
def list_carts(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    min_price: Optional[float] = Query(None, ge=0.0),
    max_price: Optional[float] = Query(None, ge=0.0),
    min_quantity: Optional[int] = Query(None, ge=0),
    max_quantity: Optional[int] = Query(None, ge=0),
):
    filtered_carts = list(carts.values())

    if min_price is not None:
        filtered_carts = [cart for cart in filtered_carts if cart.price >= min_price]
    if max_price is not None:
        filtered_carts = [cart for cart in filtered_carts if cart.price <= max_price]
    if min_quantity is not None:
        filtered_carts = [cart for cart in filtered_carts if sum(item.quantity for item in cart.items) >= min_quantity]
    if max_quantity is not None:
        filtered_carts = [cart for cart in filtered_carts if sum(item.quantity for item in cart.items) <= max_quantity]

    return filtered_carts[offset:offset+limit]

@app.post("/cart/{cart_id}/add/{item_id}")
def add_item_to_cart(cart_id: int, item_id: int):
    if cart_id not in carts:
        raise HTTPException(status_code=404, detail="Cart not found")
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    cart = carts[cart_id]
    item = items[item_id]

    for cart_item in cart.items:
        if cart_item.id == item_id:
            cart_item.quantity += 1
            break
    else:
        cart.items.append(CartItem(id=item.id, name=item.name, quantity=1, available=not item.deleted))

    cart.price += item.price
    carts[cart_id] = cart
    return {"message": "Item added to cart"}

# Item endpoints
@app.post("/item", status_code=status.HTTP_201_CREATED)
def create_item(item_json: dict, response: Response):
    #item_json = item_json[0]
    print(item_json)
    item_id = len(items.keys()) + 1
    itemm = Item(id=item_id, name=item_json['name'], price=item_json['price'])
    if item_id in items.keys():
        raise HTTPException(status_code=400, detail="Item already exists")
    items[item_id] = itemm
    response.headers["location"] = f"/item/{item_id}"
    return itemm.model_dump()

@app.get("/item/{id}")
def get_item(id: int):
    if id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    item = items[id]
    if item.deleted:
        raise HTTPException(status_code=404, detail="Item not found (deleted)")
    return item

@app.get("/item")
def list_items(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    min_price: Optional[float] = Query(None, ge=0.0),
    max_price: Optional[float] = Query(None, ge=0.0),
    show_deleted: bool = Query(False),
):
    filtered_items = list(items.values())

    if not show_deleted:
        filtered_items = [item for item in filtered_items if not item.deleted]
    if min_price is not None and max_price is not None:
        filtered_items = [item for item in filtered_items if (item.price >= min_price and item.price <= max_price)]
    if min_price is not None:
        filtered_items = [item for item in filtered_items if item.price >= min_price]
    if max_price is not None:
        filtered_items = [item for item in filtered_items if item.price <= max_price]

    return filtered_items[offset:offset+limit]

@app.put("/item/{id}")
def update_item(id: int, item_json: dict):
    if id not in items.keys():
        raise HTTPException(status_code=404, detail="Item not found")
    item = items[id]
    if item.deleted:
        raise HTTPException(status_code=304, detail="Not modifed")
    name = item_json.get("name", None)
    price = item_json.get("price", None)
    if type(name) is not str or type(price) is not float:  # lazy to create model for auto check typing...
        raise HTTPException(status_code=422, detail="Unprocessable lol")
    item.name = item_json["name"]
    item.price = item_json["price"]
    items[id] = item
    return item.model_dump()

@app.patch("/item/{id}")
def partial_update_item(id: int, item_json: dict):
    if id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    item = items[id]
    if item.deleted:
        raise HTTPException(status_code=304, detail="Not modifed")
    if "deleted" in item_json.keys():
        raise HTTPException(status_code=422, detail="Unprocessable: Can't be deleted with patch method!")
    if len(item_json.keys() - ["name", "price"]) != 0:
        raise HTTPException(status_code=422, detail="Unprocessable: you added non-existent fields")
    for field, value in item_json.items():
        setattr(items[id], field, value)
    return item.model_dump()

@app.delete("/item/{id}")
def delete_item(id: int):
    if id not in items.keys():
        return {"message": "Item's deletion mark added"}
        #raise HTTPException(status_code=404, detail="Item not found")
    item = items[id]
    if item.deleted:
        return {"message": "Item's deletion mark added"}
        #raise HTTPException(status_code=304, detail="Not modifed")
    items[id].deleted = True
    return {"message": "Item's deletion mark added"}

#if __name__ == "__main__":
#    pass
#    exit()
#    import uvicorn
#    #uvicorn.run(app, host="0.0.0.0", port=8000)
#    from fastapi.testclient import TestClient
#    client = TestClient(app)
#    response = client.post("/cart")
#    print("DSKGL IDSJGKJSDHJG HSDKJHG KSDHG KDSFHG")
#    print(response)
#    
    
