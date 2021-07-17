
from selenium import webdriver
import pyttsx3
from pyttsx3.drivers import sapi5
from googlesearch import search
import webbrowser
from datetime import datetime, timedelta
import recordatoriosAvisos
from pymongo import MongoClient, database

browser = webdriver
crearRecordatorio = False
crearTextoRecordatorio= False
crearAviso = False
crearAvisoTexto = False
crearHoraParaRecordarRecord = False
textoTemas = False
textoImportante = False
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
    print(texto)
    if(('buscar en google'in texto) or ('buscar en el navegador' in texto) or ('busca en google' in texto) or ('busca en navegador' in texto) or ('busca google' in texto) or ('busca navegador' in texto) or ('buscar google' in texto) or ('buscar navegador'in texto)):
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

    elif (('crear recordatorio' in texto) or ('nuevo recordatorio' in texto) or ('crea recordatorio' in texto)): 
        hablar("Ok. Dime en que fecha quieres crear el recordatorio")
        global crearRecordatorio
        crearRecordatorio = True
        return

    elif(crearRecordatorio == True):
        hoy = datetime.today() 
        try:
            if 'hoy' in texto:
                hablar(hoy)
                global fechaParaRecordar
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
            global crearTextoRecordatorio
            crearTextoRecordatorio = True
            crearRecordatorio = False
            hablar("Ok, ¿Qué quieres que te recuerde?")
        except: 
            print(texto)
            hablar("Ingresaste una fecha que no es válida")
            crearRecordatorio = False
        return


    elif(crearTextoRecordatorio == True):
        hablar("Ok. Creando Recordatorio")
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