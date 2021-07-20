
import re
import time
from datetime import datetime
import requests
from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()
MONGO = os.getenv("MONGO")
TOKEN = os.getenv("TOKEN")
ID = os.getenv("ID")
client = MongoClient(MONGO)
db=client.admin

miDataBase = client.test
miColeccionRecordatorios = miDataBase.recordatorios

#Funcion que sirve para mandar un mensaje a telegram con algun texto que se le pase.
def mandandoMensaje(texto: str): 
    print("Entre")
    continuar = True 
    send = texto
    id = ID
    token = TOKEN
    url = "https://api.telegram.org/bot" + token + "/sendMessage"
    params = {
        'chat_id' : id,
        'text' : send
    }
    requests.post(url, params=params)


#De esta manera borro los recordatorios que se encuentran en la base de datos. 
def borrarRecordatorio(fecha, nombre):
    global miColeccionRecordatorios 
    miColeccionRecordatorios.delete_one({"fecha": fecha, "nombre": nombre})
    time.sleep(1)


def creacionRecordatorios(texto:str, fecha, temas: str):
    global miColeccionRecordatorios
    miColeccionRecordatorios.insert_one({
        "fecha": fecha,
        "nombre": texto,
        "temas": temas
    })
