from logging import error
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
detener = False
def iniciarAsistente():
    global crearRecordatorio
    global crearTextoRecordatorio
    global nombre
    global detener

    if detener == False:
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
                        texto = ''
                    #texto= ''
            #PARECE Q FUNCIONA
            except UnboundLocalError: 
                hablar('No entendi lo que dijiste, intenta de nuevo')
                textoTk.insert(tk.END,f'{nombre}: No entendi lo que dijiste, intenta de nuevo\n')
                continue    
            except sr.UnknownValueError:
                listener = sr.Recognizer()


#Funciones que permiten el uso de hilos para evitar cierres inoportunos con la GUI
def schedule_check(t): 
    ventana.after(500,finalizo, t)

#FALTA VER COMO DETENER EL HILO, no estaria encontrando como
def finalizo(t): 
    if t.is_alive(): 
        botonTerminarAsistente['state'] = 'normal'
    if not t.is_alive() or detener == True: 
        info_label["text"] = "Asistente Inactivo"
        botonIniciarAsistente["state"] = "normal"
        botonTerminarAsistente['state'] = 'disabled'
    else:
        schedule_check(t)
    

def AsistenteIniciado():
    global detener
    detener = False
    info_label["text"] = "Asistente Virtual iniciado"
    botonIniciarAsistente["state"] = "disabled"
    t = threading.Thread(target=iniciarAsistente)
    t.setDaemon(True)
    t.start()
    schedule_check(t)

def terminarAsistente():
    botonTerminarAsistente["state"] = "disabled"
    global detener
    detener = True

nlp = stanza.Pipeline(lang='es')
#verónica es un amod o un obj
palabras_exc = ['en', 'el', 'podrias', 'deberias', 'la', 'las', 'los', 'es', 'ahi', 'aquello', 'aquellos', 'aqui', 'tu', 'tus', 'un', 'unas', 'una', 'unos']

accion_list = list()
existe_accion = False


def s_tilde(texto):
    texto = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", texto), 0, re.I)
    texto = normalize( 'NFC', texto)
    return texto

textoP = False
def acciones_IA(texto):
    global palabras_exc
    global crearRecordatorio
    global crearTextoRecordatorio
    global error
    global acciones_p 
    global existe_accion
    global detener
    global textoP


    if detener == False:
        if crearTextoRecordatorio == True: 
            textoP = True

        texto = s_tilde(texto)
        doc = nlp(texto)

        for sent in doc.sentences:
            for dep in sent.dependencies: 
                if dep[2].text:
                    accion_list.append(dep[2].text)
                    print('dep ', dep[2].text)        
        
        for sent in doc.sentences:
            for dep in sent.dependencies:
                if dep[2].text not in palabras_exc:
                    accion = dep[0].text + ' ' + dep[2].text  
                    existe_accion = True
                    acciones(accion=accion, texto=texto, accion_list=accion_list) 
                #print(accion, texto, accion_list)
        if existe_accion == False: 
            acciones_sIA(texto, accion_list)
            if error == True: 
                error = False
                return

browser = webdriver
crearRecordatorio = False
crearTextoRecordatorio= False
error = False
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

textoC= ''
dif = True

def busqueda_sIA(texto, accion_list, parar,parar_2, p_busqueda, e_busqueda, parar_3=1, parar_4=1): 
    i = 0 
    busqueda = ' '
    llego = False

    if e_busqueda not in texto: 
        pos = accion_list.index(p_busqueda)
        accion_list.insert(pos, 'en')
        #print(accion_list)
    try: 
        for accion in accion_list: 
            if llego == True: 
                if len(accion_list) > (i+1):
                    if accion_list[i+1] != p_busqueda: 
                        busqueda = busqueda + ' ' + accion
            if accion == parar or accion == parar_2 or accion == parar_3 or accion == parar_4 or parar_3 == 1 or parar_4 == 1: 
                if accion_list[i+2] == p_busqueda:
                    hablar('No comprendi lo que me solicitó, vuelva a intentarlo porfavor')
                    #probar si esto permite reiniciar la escucha por si hubo algun error cuando se definio alguna accion. 
                    error = True
                    break
                else: 
                    if accion_list[i+1] != p_busqueda:
                       llego = True
            i += 1
    except: 
        hablar('No comprendi lo que me solicitó, vuelva a intentarlo porfavor')
        error = True
        return error
    return busqueda

#acciones_IA(texto_prueba)
def acciones_sIA(texto,accion_list):
    global error
    if 'en youtube' in texto or 'youtube' in texto: 
        busqueda = busqueda_sIA(texto, accion_list, 'reproduce', 'reproducir', 'youtube', 'en youtube','buscar','buscame')
        busqueda = ''
    if 'en google' in texto or 'google' in texto:
        busqueda = busqueda_sIA(texto,accion_list, 'buscar', 'buscame','google', 'en google')
        busqueda = ''
    else: 
        if busqueda == True: 
            error = True
            return


#MODULO DE TODOS LOS COMANDOS
def acciones(accion, texto, accion_list): 
    global textoTk
    global crearRecordatorio
    global fechaParaRecordar
    global crearTextoRecordatorio
    global dif
    global textoC
    global nombre
    global textoP

    if texto != textoC:
        textoC = texto 
        dif = True 
    if textoC == texto and dif == True: 
        textoTk.insert(tk.END, texto + '\n')
        dif = False

    #Busquedas de google. No se abren paginas ni de wikipedia, ni de youtube. Ya hay otras funciones que hacen eso.
    #ANDA
    if 'dia buen' in accion or 'dias buenos' in accion: 
        hablar('Buenos días, señor')
        textoTk.insert(tk.END, f'{nombre}: Buenos días, señor\n')

    if 'tarde buena' in accion or 'tardes buenos' in accion: 
        hablar('Buenos tardes, señor')
        textoTk.insert(tk.END, f'{nombre}: Buenos tardes, señor\n')

    if 'noche buena' in accion or 'noches buenos' in accion: 
        hablar('Buenos noches, señor')
        textoTk.insert(tk.END, f'{nombre}: Buenos noches, señor\n')

    if 'ROOT hola' in accion or f'hola {nombre}' in accion: 
        hablar('Hola, señor')
        textoTk.insert(tk.END, f'{nombre}: Hola, señor\n')

    if 'estas como' in accion: 
        hablar('Muy bien')
        textoTk.insert(tk.END, f'{nombre}: Muy bien\n')
    elif 'buscar google' in accion or 'buscame google' in accion:
        hablar('Ok, realizando búsqueda')
        textoTk.insert(tk.END, f'{nombre}: Ok, realizando búsqueda\n')
        busq_list = accion_list
        while True:
            if 'google' in busq_list[0]:
                busq_list.pop(0)
                break
            else: 
                busq_list.pop(0)
        busqueda = str(busq_list)
        print('Despues: ',busqueda)
        resultadosBusquedaG = search(busqueda , lang="es", num=5,start=0, stop=12, pause=1.5 )
        resultadosBusquedaG = list(resultadosBusquedaG)   
        hablar("Búsqueda finalizada, abriendo páginas")
        textoTk.insert(tk.END, f'{nombre}: Búsqueda finalizada, abriendo páginas\n')
        num = 0
        for r in resultadosBusquedaG: 
            if num <= 5:
                if 'https://es.wikipedia.org/' in r or 'https://www.youtube.com/' in r or 'https://listado.mercadolibre.com.ar/' in r or 'https://www.mercadolibre.com.ar/' in r or 'https://www.cotodigital3.com.ar/' in r or 'https://www.manfrey.com.ar/' in r: 
                    if num != 0:
                        num -= 1
                else: 
                    webbrowser.open(r, new=2)

    
    #ANDA
    elif 'reproduce youtube' in accion or 'reproducir youtube' in accion or 'buscar youtube' in accion or 'buscame youtube' in accion:
        busq_list = accion_list
        while True:
            if 'youtube' in busq_list[0]:
                busq_list.pop(0)
                break
            else: 
                busq_list.pop(0)
        busqueda = str(busq_list)
        hablar("Ok, abriendo Youtube y Reproduciendo" + busqueda)
        textoTk.insert(tk.END, f'{nombre}:Ok, abriendo Youtube y Reproduciendo {busqueda}\n')
        pywhatkit.playonyt(busqueda)


    #Lo que permiten que se creen recordatorios y se suban a una base de datos. 
    #PROBAR, APARENTEMENTE NO ANDA
    elif 'crear recordatorio' in accion:
        hablar("Ok. Dime en que fecha quieres crear el recordatorio")
        textoTk.insert(tk.END, f'{nombre}: Ok. Dime en que fecha quieres crear el recordatorio\n')
        crearRecordatorio = True
        #accion_list.clear()
        #print('accion  dsps:', accion_list)
        return
    elif crearRecordatorio == True and accion != 'crear recordatorio':
        #hoy = datetime.today() 
        try:
            i = 0
            for palabra in accion_list: 
                if palabra in MESES:
                    accion_list[i] = str(MESES.indes(palabra) + 1)
            if 'de' in accion_list[1]: 
                accion_list[1] = 'del'
                accion_list.pop(2)
            if 'de' in accion_list[3]:
                accion_list[3] = 'del'
                accion_list.pop(4)
            fechastr=','.join(accion_list)
            fechastr= fechastr.replace(',', ' ')
            print(fechastr)
            fechaParaRecordar = datetime.strptime(fechastr, '%d del %m del %Y')
            hablar(fechaParaRecordar)           
            crearTextoRecordatorio = True
            crearRecordatorio = False
            hablar("Ok, ¿Qué quieres que te recuerde?")
            textoTk.insert(tk.END, f'{nombre}: Ok, ¿Qué quieres que te recuerde?\n')

        except: 
            hablar("Ingresaste una fecha que no es válida, cancelando operación")
            textoTk.insert(tk.END, f'{nombre}: Ingresaste una fecha que no es válida, cancelando operación\n')
            crearRecordatorio = False
        texto= ''
        return
    #ARREGLAR
    elif crearTextoRecordatorio == True and textoP == True:
        hablar("Ok. Creando Recordatorio")
        textoTk.insert(tk.END, f'{nombre}: Ok. Creando Recordatorio\n')
        recordatoriosAvisos.creacionRecordatorios(texto, fechaParaRecordar, "Sin funcionalidad de temas")
        fechaParaRecordar = ""
        crearTextoRecordatorio = False
        textoP= False

    #PROBAR COMO TOMA CADA PALABRA CON EL STANZA
    elif 'recordatorio cercano' in accion or 'recordatorio siguiente' in accion: 
    #elif (('recordatorio más cercano' in texto) or ('recordatorio cercano' in texto) or('cuál es el siguiente recordatorio' in texto) or ('cuando es el siguiente recordatorio' in texto)):
        year = datetime.today().year
        mes = datetime.today().month
        dia = datetime.today().day
        fecha = datetime(year=year, month=mes, day=dia, hour=0, minute=0, second=0,   microsecond=0)
        resultado = buscandoFecha(miColeccionRecordatorios, fecha)
        if resultado == 'No tienes ningun recordatorio cargado' :
            hablar("No tienes ningun recordatorio cargado")
            textoTk.insert(tk.END, f'{nombre}: No tienes ningun recordatorio cargado\n')
        elif resultado == 'No existen recordatorios cercanos' :
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
            textoTk.insert(tk.END, f'{nombre}: El recordatorio mas cercano es el {fecha} con el nombre {texto}\n')
            texto= ''
    accion_list.clear()
    texto = ''
    
#Funcion que permite la busqueda de la fecha mas cercana de recordatorio

def buscandoFecha(coleccion, fecha, variacion=1): 
    no_existe = 'No tienes ningun recordatorio cargado'
    try:
        if coleccion.count_docuents() == 0:
            return no_existe
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
    if audio._inLoop:
        audio.endLoop()
    audio.runAndWait()
    return 


#GUI TKINTER

if __name__ == '__main__':
    ventana = tk.Tk()
    ventana.title("Asistente Virtual")
    ventana['bg'] = '#232528'
    #ventana.geometry("500x300")
    ventana.resizable(0,0)
    ventana.iconbitmap(r'ASISTENTE/veronica.ico')
    
    botonIniciarAsistente = tk.Button( ventana, text= "Iniciar Asistente", command= AsistenteIniciado, padx=30, pady=20)
    botonIniciarAsistente.grid(row= 0, column= 0,padx=10, pady=10)
    botonIniciarAsistente['bg'] = '#EAF6FF'
    botonIniciarAsistente.config(font=("Arial", 10))

    botonTerminarAsistente = tk.Button( ventana, text='Finalizar Asistente', command=terminarAsistente, padx=30, pady=20)
    botonTerminarAsistente.grid(row=0, column=2,padx=5, pady=5)
    botonTerminarAsistente['bg'] = '#EAF6FF'
    botonTerminarAsistente.config(font=("Arial", 10))
    textoTk = tk.Text( ventana,wrap='word')
    textoTk.grid(row=2, column=0, columnspan=3, padx=10,pady=10)
    #textoTk.pack(after=botonIniciarAsistente, pady=20,padx=20, side=TOP)
    textoTk['bg'] = '#EAF6FF'
    textoTk['fg'] = '#232528'
    textoTk.config(border= 3, font=("Arial", 11),padx=6,pady=4)
    textoTk.bind("<Key>", lambda a: "break")

    info_label = tk.Label(text = "Asistente Inactivo")
    info_label['bg'] = '#232528'
    info_label['fg'] = '#EAF6FF'
    info_label.config(font=("Arial", 11))
    info_label.grid(row= 1, column= 1, pady=5)
    #info_label.pack(before=botonIniciarAsistente, pady=10)

    #info_label_F = tk.Label(text = "Asistente Activo")
    #info_label_F['bg'] = '#232528'
    #info_label_F['fg'] = '#EAF6FF'
    #info_label_F.config(font=("Arial", 11))
    #info_label_F.grid(row= 1, column= 0)
    ventana.mainloop()