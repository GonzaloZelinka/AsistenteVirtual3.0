import threading
from tkinter.constants import TOP
import speech_recognition as sr 
import tkinter as tk
from selenium import webdriver
import pyttsx3
from pyttsx3.drivers import sapi5
from googlesearch import search
import webbrowser
from datetime import datetime, timedelta
import recordatoriosAvisos
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import pywhatkit


import stanza
import re 
from unicodedata import normalize
#stanza.download('es')


#CICLO DE ESCUCHA Y FUNCIONAMIENTO
nombre = 'verónica'

def iniciarAsistente():
    global crearRecordatorio
    global crearTextoRecordatorio
    global nombre

    listener = sr.Recognizer()
    
    while True:
        try:
            with sr.Microphone() as source: 
                listener.adjust_for_ambient_noise(source, duration=1)
                voz = listener.listen(source)
                texto = listener.recognize_google(voz, language="es-ES")

                #Desactivacion del asistente:
                if ('gracias verónica' in texto.lower() or 'gracia verónica' in texto.lower() or 'gracia veronica' in texto.lower() or 'gracias veronica' in texto.lower()):
                    crearRecordatorio = False
                    crearTextoRecordatorio = False
                    hablar('De nada')
                    textoTk.insert(tk.END, 'De nada\n')
                    texto = ''
                    break
                if  texto.lower(): 
                    acciones_IA(texto.lower())
                texto= ''
        #PARECE Q FUNCIONA
        except UnboundLocalError: 
            hablar('No entendi lo que dijiste, intenta de nuevo')
            textoTk.insert(tk.END,f'{nombre}: No entendi lo que dijiste, intenta de nuevo\n')
            continue    
        except sr.UnknownValueError:
            listener = sr.Recognizer()

#Funciones que permiten el uso de hilos para evitar cierres inoportunos con la GUI
def schedule_check(t): 
    ventana.after(1000,finalizo, t)


def finalizo(t): 
    if not t.is_alive(): 
        info_label["text"] = "Asistente Inactivo"
        botonIniciarAsistente["state"] = "normal"
    else:
        schedule_check(t)

def AsistenteIniciado():
    info_label["text"] = "Asistente Virtual iniciado"
    botonIniciarAsistente["state"] = "disabled"
    t = threading.Thread(target=iniciarAsistente)
    t.start()
    schedule_check(t)





nlp = stanza.Pipeline(lang='es')
#verónica es un amod o un obj
palabras_exc = ['en', 'el', 'podrias', 'deberias', 'la', 'las', 'los', 'es', 'ahi', 'aquello', 'aquellos', 'aqui', 'tu', 'tus', 'un', 'unas', 'una', 'unos']
saludo = ['hola', 'buen dia', 'buenos dias', 'buenas tardes']
texto_prueba = 'verónica como estas podrias buscar en google que es el cancer'
accion_list = list()


def s_tilde(texto):
    texto = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", texto), 0, re.I)
    texto = normalize( 'NFC', texto)
    return texto


def acciones_IA(texto):
    global palabras_exc
    global crearRecordatorio
    global crearTextoRecordatorio

    if crearRecordatorio == True or crearTextoRecordatorio == True: 
        return
    texto = s_tilde(texto)
    doc = nlp(texto)

    for sent in doc.sentences:
        for dep in sent.dependencies: 
            if dep[2].text:
                accion_list.append(dep[2].text)        
#probar el tema de que en la lista se pueda ver el buen dia. Con el de accion funciona
    for sent in doc.sentences:
        for dep in sent.dependencies:
            if dep[2].text not in palabras_exc:
                accion = dep[0].text + ' ' + dep[2].text  
                acciones(accion=accion, texto=texto, accion_list=accion_list) 
            #print(accion, texto, accion_list)

browser = webdriver
crearRecordatorio = False
crearTextoRecordatorio= False

now = datetime.now()
fechaParaRecordar = datetime.now()
horaParaRecordarRecord = ""
horaParaRecordar = ""
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
load_dotenv()
MONGO = os.getenv("MONGO")
client = MongoClient(MONGO)
db=client.admin

miDataBase = client.test
miColeccionRecordatorios = miDataBase.recordatorios



#acciones_IA(texto_prueba)

#MODULO DE TODOS LOS COMANDOS
def acciones(accion, texto, accion_list): 
    global textoTk
    global crearRecordatorio
    global fechaParaRecordar
    global crearTextoRecordatorio

    textoTk.insert(tk.END, texto + '\n')

    #Busquedas de google. No se abren paginas ni de wikipedia, ni de youtube. Ya hay otras funciones que hacen eso.
    #ANDA
    if 'dia buen' in accion or 'dias buenos' in accion: 
        hablar('Buenos días, señor')
        return
    if 'tarde buena' in accion or 'tardes buenos' in accion: 
        hablar('Buenos tardes, señor')
        return
    if 'noche buena' in accion or 'noches buenos' in accion: 
        hablar('Buenos noches, señor')
        return
    elif 'ROOT hola' in accion: 
        hablar('Hola, señor')
        return
    elif 'buscar google' in accion:
        hablar('Ok, realizando búsqueda')
        busq_list = accion_list
        while True:
            if 'google' in busq_list[0]:
                busq_list.pop(0)
                print('Se borro: ', busq_list[0])
                break
            else: 
                print('Se borro: ', busq_list[0])
                busq_list.pop(0)
        busqueda = str(busq_list)
        print('Despues: ',busqueda)
        resultadosBusquedaG = search(busqueda , lang="es", num=5,start=0, stop=12, pause=1.5 )
        resultadosBusquedaG = list(resultadosBusquedaG)   
        hablar("Búsqueda finalizada, abriendo páginas")
        textoTk.insert(tk.END, f'{nombre}: Ok, abriendo páginas\n')
        num = 0
        for r in resultadosBusquedaG: 
            if num <= 5:
                if 'https://es.wikipedia.org/' in r or 'https://www.youtube.com/' in r or 'https://listado.mercadolibre.com.ar/' in r or 'https://www.mercadolibre.com.ar/' in r or 'https://www.cotodigital3.com.ar/' in r or 'https://www.manfrey.com.ar/' in r: 
                    if num != 0:
                        num -= 1
                else: 
                    webbrowser.open(r, new=2)
        return
    
    #ANDA
    elif 'reproduce youtube' in accion or 'reproducir youtube' in accion:
        busq_list = accion_list
        while True:
            if 'youtube' in busq_list[0]:
                busq_list.pop(0)
                print('Se borro: ', busq_list[0])
                break
            else: 
                print('Se borro: ', busq_list[0])
                busq_list.pop(0)
        busqueda = str(busq_list)
        hablar("Ok, abriendo Youtube y Reproduciendo" + busqueda)
        textoTk.insert(tk.END, f'{nombre}:Ok, abriendo Youtube y Reproduciendo {busqueda}\n')
        pywhatkit.playonyt(busqueda)
        return

    #Lo que permiten que se creen recordatorios y se suban a una base de datos. 
    #PROBAR, APARENTEMENTE NO ANDA
    elif 'crear recordatorio' in accion:
        hablar("Ok. Dime en que fecha quieres crear el recordatorio")
        textoTk.insert(tk.END, f'{nombre}: Ok. Dime en que fecha quieres crear el recordatorio\n')
        crearRecordatorio = True
        return
    elif(crearRecordatorio == True):
        hoy = datetime.today() 
        try:
            i = 0
            for palabra in accion_list: 
                if palabra in MESES:
                    accion_list[i] = str(MESES.indes(palabra) + 1)
            accion_list[1] = 'del'
            accion_list[3] = 'del'
            fechastr=','.join(accion_list)
            fechastr= fechastr.replace(',', ' ')
            fechaParaRecordar = datetime.strptime(fechastr, '%d del %m del %Y')
            hablar(fechaParaRecordar)           
            crearTextoRecordatorio = True
            crearRecordatorio = False
            hablar("Ok, ¿Qué quieres que te recuerde?")
            textoTk.insert(tk.END, f'{nombre}: Ok, ¿Qué quieres que te recuerde?\n')
            return
        except: 
            hablar("Ingresaste una fecha que no es válida, cancelando operación")
            textoTk.insert(tk.END, f'{nombre}: Ingresaste una fecha que no es válida, cancelando operación\n')
            crearRecordatorio = False
            return      
    elif(crearTextoRecordatorio == True):
        hablar("Ok. Creando Recordatorio")
        textoTk.insert(tk.END, f'{nombre}: Ok. Creando Recordatorio\n')
        recordatoriosAvisos.creacionRecordatorios(texto, fechaParaRecordar, "Sin funcionalidad de temas")
        fechaParaRecordar = ""
        crearTextoRecordatorio = False
    
    #PROBAR COMO TOMA CADA PALABRA CON EL STANZA
    elif (('recordatorio más cercano' in texto) or ('recordatorio cercano' in texto) or('cuál es el siguiente recordatorio' in texto) or ('cuando es el siguiente recordatorio' in texto)):
        year = datetime.today().year
        mes = datetime.today().month
        dia = datetime.today().day
        fecha = datetime(year=year, month=mes, day=dia, hour=0, minute=0, second=0,   microsecond=0)
        resultado = buscandoFecha(miColeccionRecordatorios, fecha)
        if resultado == 'No existen recordatorios cercanos' :
            hablar("No existen recordatorios cercanos")
            textoTk.insert(tk.END, f'{nombre}: No existen recordatorios cercanos\n')
        else: 
            resultado = str(resultado)
            resultado = resultado.replace("'", '')
            resultado = resultado.replace(",", '')
            resultado = resultado.replace("datetime.datetime(", '')
            resultado = resultado.replace(")", '')
            resultado = resultado.split()
            resultado.pop(0)
            resultado.pop(0)
            resultado.pop(0)
            resultado.pop()
            resultado.pop()
            resultado.pop()
            resultado.pop()
            resultado.pop()
            anio = int(resultado[0])
            mes = int(resultado[1])
            dia = int(resultado [2])
            c = 0
            texto = ''
            for r in resultado:
                if c > 5: 
                    texto = texto + ' ' + resultado[c]
                c += 1
            fecha= datetime(anio,mes,dia)
            hablar('El recordatorio mas cercano es el ')
            hablar(fecha)
            hablar('con el nombre' + texto)
            textoTk.insert(tk.END, f'{nombre}: El recordatorio mas cercano es el {fecha} conel    nombre {texto}\n')
            texto= ''
    texto = ''

#Funcion que permite la busqueda de la fecha mas cercana de recordatorio

def buscandoFecha(coleccion, fecha, variacion=1): 
    try:
        fecha_b = fecha + timedelta(days=variacion)
        resultado = coleccion.find({"fecha": {"$gte": fecha_b}}).sort([('fecha',1)])
        resultado = list(resultado)
        assert len(resultado) >=1 
        return resultado[0]
    except: 
        if variacion >= 100:
            no_hay = 'No existen recordatorios cercanos'
            return no_hay
        return buscandoFecha(coleccion, fecha, variacion = variacion*2)


def hablar(texto):
    audio = pyttsx3.init()
    nuevaRate = 200
    voices = audio.getProperty('voices')
    audio.setProperty('voice', voices[2].id)
    audio.setProperty('rate', nuevaRate)
    audio.say(text=texto)
    audio.runAndWait()
    return 


#GUI TKINTER

if __name__ == '__main__':
    ventana = tk.Tk()
    ventana.title("Asistente Virtual")
    ventana['bg'] = '#232528'
    ventana.geometry("500x300")
    ventana.resizable(0,0)
    ventana.iconbitmap(r'ASISTENTE/veronica.ico')

    botonIniciarAsistente = tk.Button(ventana, text= "Iniciar Asistente", command= AsistenteIniciado, padx=30, pady=20)
    botonIniciarAsistente.pack()
    botonIniciarAsistente['bg'] = '#EAF6FF'
    botonIniciarAsistente.config(font=("Arial", 10))
    textoTk = tk.Text(ventana, height= 150, width=150,wrap='word')
    textoTk.pack(after=botonIniciarAsistente, pady=20,padx=20, side=TOP)
    textoTk['bg'] = '#EAF6FF'
    textoTk['fg'] = '#232528'
    textoTk.config(border= 3, font=("Arial", 11),padx=6,pady=4)
    textoTk.bind("<Key>", lambda a: "break")

    info_label = tk.Label(text = "Asistente Inactivo")
    info_label['bg'] = '#232528'
    info_label['fg'] = '#EAF6FF'
    info_label.config(font=("Arial", 11))
    info_label.pack(before=botonIniciarAsistente, pady=10)

    ventana.mainloop()