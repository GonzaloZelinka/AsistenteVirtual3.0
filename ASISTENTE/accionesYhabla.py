
from selenium import webdriver
import pyttsx3
from pyttsx3.drivers import sapi5
from googlesearch import search
import webbrowser
from datetime import datetime
import recordatoriosAvisos

browser = webdriver
crearRecordatorio = False
crearTextoRecordatorio= False
crearAviso = False
crearAvisoTexto = False
crearHoraParaRecordarRecord = False
textoTemas = False
textoImportante = False
now = datetime.now()
fechaParaRecordar = ""
horaParaRecordarRecord = ""
horaParaRecordar = ""
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

#MODULO DE TODOS LOS COMANDOS
def acciones(texto: str): 
    if('buscar en google' or 'buscar en el navegador' or 'busca en google' or 'busca en navegador' or 'busca google' or 'busca navegador' or 'buscar google' or 'buscar navegador') in texto:
        palabras = texto.split()
        contadorPalabras = len(palabras)
        if (contadorPalabras > 3):
            texto = texto.replace("buscar en google", "")
            resultadosBusquedaG = search(texto , tld="com", lang="es", num=5,start=0, stop=5, pause=3.0 )
            hablar("Ok, abriendo 5 paginas")
            for r in resultadosBusquedaG: 
                if (r == 1): 
                    webbrowser.open(r, new=1)
                else:
                    webbrowser.open_new_tab(r)
        else:
            hablar("No me haz dicho que quieres que busque. Repítelo, por favor")
        return

    elif ('crear recordatorio' or 'recordatorio' or 'nuevo recordatorio' or 'crea recordatorio' or 'recordame') in texto: 
        hablar("Ok. Dime en que fecha quieres crear el recordatorio")
        global crearRecordatorio
        crearRecordatorio = True
        return

    elif(crearRecordatorio == True):
        hoy = datetime.today() 
        try:
            print('texto:', texto)
            if 'hoy' in texto:
                hablar(hoy)
                global fechaParaRecordar
                fechaParaRecordar = hoy.strftime('%Y-%m-%d')
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
                fechaParaRecordar = fechaParaRecordar.strftime('%Y-%m-%d')
                hablar(fechaParaRecordar)
                print('fecha para recordar:',fechaParaRecordar)             
            global crearTextoRecordatorio
            crearTextoRecordatorio = True
            crearRecordatorio = False
            hablar("Ok, ¿Qué quieres que te recuerde?")
        except: 
            hablar("Ingresaste una fecha que no es válida")
            crearRecordatorio = False
        return


    elif(crearTextoRecordatorio == True):
        hablar("Ok. Creando Recordatorio")
        recordatoriosAvisos.creacionRecordatorios(texto, fechaParaRecordar, "Sin funcionalidad de temas")
        fechaParaRecordar = ""
        crearTextoRecordatorio = False

    


#Funcion que permite que el asistente pueda comunicarse
def hablar(texto:str):
    print("Hablando...")
    audio = pyttsx3.init()
    nuevaRate = 210
    voices = audio.getProperty('voices')
    audio.setProperty('voice', voices[2].id)
    audio.setProperty('rate', nuevaRate)
    audio.say(text=texto)
    audio.runAndWait()
    return 