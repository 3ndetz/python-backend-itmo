from fastapi import FastAPI, Response, WebSocket, HTTPException, Query, APIRouter
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
    items: List[CartItem]
    price: float


cart = APIRouter(prefix='/cart')

print("lol")


# Cart endpoints
@cart.post("/", status_code=HTTPStatus.CREATED)
async def create_cart(response: Response):
    cart_id = len(carts) + 1
    carts[cart_id] = Cart(id=cart_id, items=[], price=0)
    response.headers['location'] = f'/cart/{cart.id}'
    response.headers['id'] = cart_id
    print("created cart",card_id)
    return response

    
app.include_router(cart)

@app.get("/cart/{id}")
async def get_cart(id: int):
    if id not in carts:
        raise HTTPException(status_code=404, detail="Cart not found")
    return carts[id]


@app.get("/cart")
async def list_carts(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_quantity: Optional[int] = None,
    max_quantity: Optional[int] = None
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
async def add_item_to_cart(cart_id: int, item_id: int):
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
    return {"message": "Item added to cart"}

# Item endpoints
@app.post("/item")
async def create_item(item: Item):
    if item.id in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items[item.id] = item
    return item

@app.get("/item/{id}")
async def get_item(id: int):
    if id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[id]

@app.get("/item")
async def list_items(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    show_deleted: bool = False
):
    filtered_items = list(items.values())

    if not show_deleted:
        filtered_items = [item for item in filtered_items if not item.deleted]
    if min_price is not None:
        filtered_items = [item for item in filtered_items if item.price >= min_price]
    if max_price is not None:
        filtered_items = [item for item in filtered_items if item.price <= max_price]

    return filtered_items[offset:offset+limit]

@app.put("/item/{id}")
async def update_item(id: int, item: Item):
    if id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[id] = item
    return item

@app.patch("/item/{id}")
async def partial_update_item(id: int, item: Item):
    if id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    stored_item = items[id]
    update_data = item.dict(exclude_unset=True)
    update_data.pop('deleted', None)  # Ensure 'deleted' field can't be changed
    for field, value in update_data.items():
        setattr(stored_item, field, value)
    return stored_item

@app.delete("/item/{id}")
async def delete_item(id: int):
    if id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[id].deleted = True
    return {"message": "Item marked as deleted"}

# WebSocket Chat
chat_rooms = {}

@app.websocket("/chat/{chat_name}")
async def websocket_endpoint(websocket: WebSocket, chat_name: str):
    await websocket.accept()
    if chat_name not in chat_rooms:
        chat_rooms[chat_name] = []

    username = f"User_{random.randint(1000, 9999)}"
    chat_rooms[chat_name].append((websocket, username))

    try:
        while True:
            data = await websocket.receive_text()
            for client, _ in chat_rooms[chat_name]:
                if client != websocket:
                    await client.send_text(f"{username} :: {data}")
    finally:
        chat_rooms[chat_name].remove((websocket, username))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
