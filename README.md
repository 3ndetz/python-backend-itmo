# Python Backend Course 

# Prerequirements

You need installed:
- python 3.12
- - As main interpreter added to PATH, so you could run `python3.12 --version`
- poetry
- makefile

(Run & developed on Windows WSL2 Ubuntu)

## Clone the repo

```
cd your_workfolder

git clone https://github.com/3ndetz/python-backend-itmo
```

## Prepare to run

Enter the folder and check installations and virtual env. Ensure you have `python3.12` into the path with `python3.12 --version`!

```
cd python-backend-itmo

make installation
```

# Run apps

When you prepared for run (check previous section), then you can run other apps (homeworks).

## Homework 3

Used hw2 fastapi shop service for creating graphs.

See the screenshots with graphs in the [PR](https://github.com/3ndetz/python-backend-itmo/pull/2) for hw2.

If you want to start the services yourself, follow the guide below.

Firstly ensure you haven't running services on the 9090, 3000 and 8000 ports.

To run services in docker use:

1. `cd python-backend-itmo`

2. `docker compose -f "docker-compose.yml" up -d`

- To open prometheus you can go to `localhost:9090`

- To open Graphana you can go to `localhost:3000`

- - To see this service's working graphs, go the `Connections` section, `Data sources` and add a new `Prometheus` connection.
- - Add `http://prometheus:9090/` url to this connection.
- - Now you can open it in graphana in the `Explore` section and create graphs yourself

## Homework 2

For additional info and screnshoots see [pull request ](https://github.com/3ndetz/python-backend-itmo/pull/1) of hw2.

To test homework 1 open another terminal & run testing script:

`cd python-backend-itmo`

`make test_hw2`

To test additional websocket task:

`make test_hw2_ws`

And to see outputs of test messages (in rooms) you can run inner test:

`make hw21runInnerTest`

Files of this hws are located in the `hw2` branch of this repo:

`repo/lecture_2/hw/shop_api/main.py`

`repo/lecture_2/hw/shop_api/ws_rooms.py`


## Homework 1

To test homework 1 open another terminal & run testing script:

`cd python-backend-itmo`

`make test_hw1`

(`make test test_hw1_val` with some additional value tests)

### Screenshots

If scripts somehow is not working.

![hw1screen](screenshots/hw1/1_asgi_tests_result.png)

---

# Additional / original info

#### Лекция 1 - Основы сети и Python Backend

Реализовать "Математическое API" из примера напрямую через ASGI-compatible
функцию. В частности

- запросы, для которых нет обработчиков (не тот метод, не тот путь) должны
  возвращать ошибку `404 Not Found`
- запрос `GET /factorial` (n!)
  - возвращается в тело запроса в формате json вида `{"result": 123}`
  - в query-параметре запроса должен быть параметр `n: int`
  - если параметра нет, или он не является числом - возвращаем `422
    Unprocessable Entity`
  - если параметр не валидное число (меньше 0) - возвращаем `400 Bad Request`
- запрос `GET /fibonacci` (n-ое число fibonacci)
  - возвращается в тело запроса в формате json вида `{"result": 123}`
  - в path-параметре запроса (`fibonacci/{n}`) должен быть параметр `n: int`
  - если параметра нет, или он не является числом - возвращаем `422
    Unprocessable Entity`
  - если параметр не валидное число (меньше 0) - возвращаем `400 Bad Request`
- запрос `GET /mean` (среднее массива)
  - возвращается в тело запроса в формате json вида `{"result": 123}`
  - в теле запроса не пустой массив из `float`'ов (например `[1, 2.3, 3.6]`)
  - тело не является массивом `float`'ов - возвращаем `422
    Unprocessable Entity`
  - если массив пустой - возвращаем `400 Bad Request`

Болванка для начала:

```python
async def app(scope, receive, send) -> None:
    ...
```

В репозитории так же должна быть организована работа с зависимостями (хотя бы
`requirements.txt`).

Стоит так же заранее прописать (в коде или `README.md`), как запустить
приложение (например: `uvicorn main:app`).

- [Спецификация ASGI](https://asgi.readthedocs.io/en/latest/specs/www.html#http)
- [Исходный код API на FastAPI](/lecture_1/math_example.py)
- [Тесты для первого ДЗ (pytest)](/tests/test_homework_1.py)

Чтобы протестировать свое ДЗ или работу примера на FastAPI - в одном терминале
запустите приложение (например `uvicorn lecture_1.math_example:app`), а в другом
выполните `pytest`.
