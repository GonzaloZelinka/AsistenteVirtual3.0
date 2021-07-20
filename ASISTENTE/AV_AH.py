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


#CICLO DE ESCUCHA Y FUNCIONAMIENTO
nombre = 'verónica'

def iniciarAsistente():
    global crearRecordatorio
    global crearTextoRecordatorio
    global nombre

    listener = sr.Recognizer()
    
    Llamado = False
    while True:
        try:
            with sr.Microphone() as source: 
                listener.adjust_for_ambient_noise(source, duration=1)
                voz = listener.listen(source)
                texto = listener.recognize_google(voz, language="es-ES")

                #Desactivacion del asistente:
                if Llamado == True: 
                    if (('gracias verónica' in texto.lower()) or ('gracia verónica' in texto.lower()) or ('gracia veronica' in texto.lower()) or ('gracias veronica' in texto.lower()) or ('gracias vero' in texto.lower()) or ('gracia vero'in texto.lower()) or ('gracias'in texto.lower())):
                        Llamado = False
                        crearRecordatorio = False
                        crearTextoRecordatorio = False
                        hablar('De nada')
                        textoTk.insert(tk.END, 'De nada\n')
                        texto = ''
                        break
                    acciones(texto.lower())
                if nombre.lower() in texto.lower(): 
                    hablar("Si, ¿qué necesitas?")
                    textoTk.insert(tk.END, f'{nombre}: Si, ¿qué necesitas?\n')
                    Llamado = True
                texto= ''
        except sr.UnknownValueError:
            textoTk.insert(tk.END, texto + '\n')
            listener = sr.Recognizer()


#Funciones que permiten el uso de hilos para evitar cierres inoportunos con la GUI
def schedule_check(t): 
    ventana.after(1000,finalizo, t)


def finalizo(t): 
    if not t.is_alive(): 
        info_label["text"] = "Asistente Inactivo"
        botonIniciarAsistente["state"] = "normal"
        print('hilo muerto')
    else:
        print('hilo vivo')
        schedule_check(t)

def AsistenteIniciado():
    info_label["text"] = "Asistente Virtual iniciado"
    botonIniciarAsistente["state"] = "disabled"
    t = threading.Thread(target=iniciarAsistente)
    t.start()
    schedule_check(t)


#ACCIOONES QUE PERMITE EL AV
browser = webdriver
crearRecordatorio = False
crearTextoRecordatorio= False
now = datetime.now()
fechaParaRecordar = datetime.now()
horaParaRecordarRecord = ""
horaParaRecordar = ""
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

client = MongoClient("mongodb+srv://admin:43789663@asistentevirtualcluster.yioiu.mongodb.net/test?retryWrites=true&w=majority")
db=client.admin

miDataBase = client.test
miColeccionRecordatorios = miDataBase.recordatorios

#MODULO DE TODOS LOS COMANDOS
def acciones(texto: str): 
    global textoTk
    global crearRecordatorio
    global fechaParaRecordar
    global crearTextoRecordatorio

    textoTk.insert(tk.END, texto + '\n')
    if(('buscar en google' in texto) or ('buscar en el navegador' in texto) or ('busca en google' in texto) or ('busca en navegador' in texto) or ('busca google' in texto) or ('busca navegador' in texto) or ('buscar google' in texto) or ('buscar navegador'in texto)):
        palabras = texto.split()
        contadorPalabras = len(palabras)
        if (contadorPalabras > 3):
            texto = texto.replace("buscar en google", "")
            resultadosBusquedaG = search(texto , tld="com", lang="es", num=5,start=0, stop=5, pause=3.0 )
            hablar("Ok, abriendo 5 paginas")
            textoTk.insert(tk.END, f'{nombre}: Ok, abriendo 5 paginas\n')
            for r in resultadosBusquedaG: 
                if (r == 1): 
                    webbrowser.open(r, new=1)
                else:
                    webbrowser.open_new_tab(r)
        else:
            hablar("No me haz dicho que quieres que busque. Repítelo, por favor")
            textoTk.insert(tk.END, f'{nombre}: No me haz dicho que quieres que busque. Repítelo, por favor\n')
        return
    #elif (('reproducir' in texto) or (''))
    elif (('crear recordatorio' in texto) or ('nuevo recordatorio' in texto) or ('crea recordatorio' in texto)): 
        hablar("Ok. Dime en que fecha quieres crear el recordatorio")
        textoTk.insert(tk.END, f'{nombre}: Ok. Dime en que fecha quieres crear el recordatorio\n')
        crearRecordatorio = True
        return

    elif(crearRecordatorio == True):
        hoy = datetime.today() 
        try:
            if 'hoy' in texto:
                hablar(hoy)
                fechaParaRecordar = hoy
            else: 
                lista_fecha = texto.split()
                for palabra in lista_fecha: 
                    if palabra in MESES:
                        texto = texto.replace(palabra, str(MESES.index(palabra) + 1))
                lista_fecha = texto.split()
                lista_fecha[1] = 'del'
                lista_fecha[3] = 'del'

                fechastr=','.join(lista_fecha)
                fechastr= fechastr.replace(',', ' ')
                fechaParaRecordar = datetime.strptime(fechastr, '%d del %m del %Y')
                hablar(fechaParaRecordar)           
            crearTextoRecordatorio = True
            crearRecordatorio = False
            hablar("Ok, ¿Qué quieres que te recuerde?")
            textoTk.insert(tk.END, f'{nombre}: Ok, ¿Qué quieres que te recuerde?\n')
        except: 
            hablar("Ingresaste una fecha que no es válida")
            textoTk.insert(tk.END, f'{nombre}: Ingresaste una fecha que no es válida\n')
            crearRecordatorio = False
        return


    elif(crearTextoRecordatorio == True):
        hablar("Ok. Creando Recordatorio")
        textoTk.insert(tk.END, f'{nombre}: Ok. Creando Recordatorio\n')
        recordatoriosAvisos.creacionRecordatorios(texto, fechaParaRecordar, "Sin funcionalidad de temas")
        fechaParaRecordar = ""
        crearTextoRecordatorio = False
    elif (('recordatorio más cercano' in texto) or ('recordatorio cercano' in texto) or ('cuál es el siguiente recordatorio' in texto) or ('cuando es el siguiente recordatorio' in texto)):
        year = datetime.today().year
        mes = datetime.today().month
        dia = datetime.today().day
        fecha = datetime(year=year, month=mes, day=dia, hour=0, minute=0, second=0, microsecond=0)

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
            textoTk.insert(tk.END, f'{nombre}: El recordatorio mas cercano es el {fecha} con el nombre {texto}\n')
            texto= ''
    texto = ''
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


#Funcion que permite que el asistente pueda comunicarse
def hablar(texto):
    audio = pyttsx3.init()
    nuevaRate = 210
    voices = audio.getProperty('voices')
    audio.setProperty('voice', voices[2].id)
    audio.setProperty('rate', nuevaRate)
    audio.say(text=texto)
    audio.runAndWait()
    return 


#GUI TKINTER
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