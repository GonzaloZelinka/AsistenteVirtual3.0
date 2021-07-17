
import re
import time
from datetime import timedelta, datetime
import requests
from pymongo import MongoClient
 
# SUPER INTERESANTE; URL PARA Q ME DESCARGUE EL CALENDARIO DE MI FACU DE MOODLE
#https://frre.cvg.utn.edu.ar/calendar/export_execute.php?userid=10901&authtoken=4858854c87f15d990be1541add85eb58efc32bd7&preset_what=all&preset_time=custom
#PUEDO IR ACTUALIZANDO EL ARCHIVO AUTOMATICAMENTE; Y ASI VOY HACIENDO AVISOS DE LOS TEMAS

client = MongoClient("mongodb+srv://admin:43789663@asistentevirtualcluster.yioiu.mongodb.net/test?retryWrites=true&w=majority")
db=client.admin

miDataBase = client.test
miColeccionRecordatorios = miDataBase.recordatorios

#Funcion que sirve para mandar un mensaje a telegram con algun texto que se le pase.
def mandandoMensaje(texto: str): 
    print("Entre")
    continuar = True 
    send = texto
    id = "1723938527"
    token = "1784647110:AAH1vLJr5trSw8cDC-IKdeZLl3a20iVVlVo"
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
