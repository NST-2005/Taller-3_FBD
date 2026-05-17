from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

#os.environ para despliegue. Descomente cuando ya probó todo local.
#client = MongoClient(os.environ["MONGO_URI"])
# TODO: conectarse al cluster Admonsis  
client = MongoClient("mongodb://ISIS2304I30202610:j8Wlhaambdcp@157.253.236.88:8087")

# TODO: conectarse a la base de datos Admonsis  
# db = client["ISIS*******"]
db = client["ISIS2304I30202610"]

@app.get("/")
def inicio():
    return {"Estado": "API funcionando correctamente"}

@app.get("/proveedores")
def get_proveedores():
    proveedores=list(db["proveedores"].find({}, {"_id":0}))
    return proveedores

@app.get("/proveedores/{bebida_id}")
def get_proveedor_bebida(bebida_id:int):
    proveedor = db["proveedores"].find_one({"bebidas_suministradas":bebida_id},{"_id":0})   
    return proveedor or {} 

@app.post("/proveedores")
def post_proveedor(datos:dict):
    datos["fecha_registro"]= datetime.now().isoformat()
    db["proveedores"].insert_one(datos)
    return {"mensaje":"Proveedor registrado"}

@app.put("/proveedores/{nombre}")
def update_proveedor(nombre:str, datos:dict):
    resultado = db["proveedores"].replace_one({"nombre": nombre}, datos)
    return {"mensaje": "Proveedor actualizado correctamente"} 

@app.patch("/proveedores/{nombre}")
def patch_proveedor(nombre: str, datos: dict):
    resultado = db["proveedores"].update_one({"nombre": nombre}, {"$set": datos})
    return {"mensaje": "Campos actualizado correctamente"}

@app.delete("/proveedores/{nombre}")
def delete_proveedor(nombre: str):
    resultado = db["proveedores"].delete_one({"nombre": nombre})
    return {"mensaje": f"Proveedor {nombre} eliminado correctamente"}

# ---BARES---

@app.get("/bares")
def get_bares():
    bares=list(db["bares"].find({}, {"_id":0}))
    return bares

@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: str):
    comentarios = list(db["comentarios"].find(
        {"bar_id": bar_id},
        {"_id": 0}
    ))
    return comentarios


@app.post("/bares")
def post_bares(datos:dict):
    datos["fecha_registro"]= datetime.now().isoformat()
    db["bares"].insert_one(datos)
    return {"mensaje":"Bar registrado correctamente"}

@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: str, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha']  = datetime.now().isoformat()
    db["comentarios"].insert_one(datos)
    return {'mensaje': 'Comentario guardado'}


#---EVENTOS BARES ---
# GET - retornar eventos de un bar  
@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: str):
    eventos = list(db["eventos"].find(
        {"bar_id": bar_id},
        {"_id": 0}
    ))
    return eventos

# POST - registrar un evento
@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: str, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha_creacion'] = datetime.now().isoformat()
    db["eventos"].insert_one(datos)
    return {'mensaje': 'Evento registrado'}