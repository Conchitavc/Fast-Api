import io
from enum import Enum
from random import random
from typing import Dict, Optional

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import ORJSONResponse, UJSONResponse
from starlette.responses import HTMLResponse, StreamingResponse


app = FastAPI()


class RoleName(str, Enum):
    Admin = 'Admin'
    Writer = 'Writer'
    Reader = 'Reader'


class Operacion(str, Enum):
    Sumar = '+'
    Restar = '-'
    Multiplicar = '*'
    Dividir = '/'


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    Price: float
    tax: Optional[float] = None


@app.get("/")
def root():
    return {"message": "hello world, from galileo master!! section V"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int) -> Dict[str, int]:
#    return {"item_id": item_id}


@app.get("/users/me")
def read_current_user():
    return {"user_id": "te current logged user"}


@app.get("/users/{user_id}")
def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/roles/{role_name}")
def get_role_permissions(role_name: RoleName):
    # return role permission
    if role_name == RoleName.Admin:
        return {"role_name": role_name, "permissions": "Full access"}
    if role_name == RoleName.Writer:
        return {"role_name": role_name, "permissions": "writer access"}
    return {"role_name": role_name, "permissions": "Read access only"}


fake_items_db = [{"item_name": "uno"}, {"item_name": "dos"}, {"item_name": "tres"}]


@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@app.get("/items/{item_id}")
def read_item(item_id: int, query: Optional[str] = None):
    message = {"item_id": item_id}
    if query:
        message['query'] = query

    return message


@app.get("/users/{user_id}/items/{item_id}")
def read_user_item(user_id: int, item_id: int, query: Optional[str] = None, describe: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}

    if query:
        item['query'] = query

    if describe:
        item['description'] = "this is a long description for the item"

    return item


#@app.post()
#def create_item(item: Item):
#    return {
#        "message": "The item was successfully created",
#        "item": item.dict()
#    }


@app.post("/items/")
def create_item(item: Item):
    if not item.tax:
        item.tax = item.price * 0.12

    return {"item_id": random.randint(1, 100), **item.dict()}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item.tax == 0 or item.tax is None:
        item.tax = item.price * 0.12

    return {
        "message": "the item was update",
        "item_id": item_id,
        "item": item.dict()
    }


@app.get("/itemsall", response_class=UJSONResponse)
def read_long_json():
    return [{"item_id": "item"}, {"item_id": "item"}, {"item_id": "item"},
            {"item_id": "item"}, {"item_id": "item"}, {"item_id": "item"},
            {"item_id": "item"}, {"item_id": "item"}, {"item_id": "item"},
            {"item_id": "item"}, {"item_id": "item"}, {"item_id": "item"}]


@app.get("/html", response_class=HTMLResponse)
def read_html():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """


@app.get("/csv")
def get_csv():
    df = pd.DataFrame({"Column A": [1, 2], "Column B": [3, 4]})

    stream = io.StringIO()

    df.to_csv(stream, index=False)

    response = StreamingResponse(iter([stream.getvalue()]), media_type='text/csv')

    response.headers['Content-Disposition'] = "attachment; filename=my_awesome_report.csv"

    return response


@app.get("/calculadora/{operacion}")
def read_operation(Operando: int, TipoOperacion: Operacion, Operador: int):
    if TipoOperacion == Operacion.Sumar:
        Resultado = Operando + Operador
    if TipoOperacion == Operacion.Restar:
        Resultado = Operando - Operador
    if TipoOperacion == Operacion.Multiplicar:
        Resultado = Operando * Operador
    if TipoOperacion == Operacion.Dividir:
        Resultado = Operando / Operador
    return {"Su resultado es:", Resultado}


@app.post("/calculadora/{operacion}")
def read_operation_post(Operando: int, TipoOperacion: Operacion, Operador: int):
    """

    :type Operador: object
    """
    if TipoOperacion == Operacion.Sumar:
        Resultado = Operando + Operador
    if TipoOperacion == Operacion.Restar:
        Resultado = Operando - Operador
    if TipoOperacion == Operacion.Multiplicar:
        Resultado = Operando * Operador
    if TipoOperacion == Operacion.Dividir:
        Resultado = Operando / Operador
    return {"Su resultado es:", Resultado}

