
from selenium import webdriver
import time 
import pyttsx3
from pyttsx3.drivers import sapi5
from googlesearch import search
import webbrowser
import datetime
import recordatoriosAvisos

browser = webdriver
validarBusquedaG = False
crearRecordatorio = False
crearTextoRecordatorio= False
crearAviso = False
crearAvisoTexto = False
crearHoraParaRecordarRecord = False
textoTemas = False
textoImportante = False
now = datetime.datetime.now()
fechaParaRecordar = ""
horaParaRecordarRecord = ""
horaParaRecordar = ""
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "noviembre", "diciembre"]


#MODULO DE TODOS LOS COMANDOS
def acciones(texto: str): 
    if texto.__contains__("espera"):
        if texto.__contains__("minuto"):
            hablar("Ok. Esperando 1 minuto")
            time.sleep(60)
        elif texto.__contains__("minutos"):
            texto = texto.replace("espera", "")
            texto = texto.replace("minutos", "")
            hablar("Ok. Esperando "+ texto + "minutos")
            tiempo = int(texto)
            tiempo = tiempo * 60
            time.sleep(tiempo)
        else:
            hablar("Ok. Esperando por defecto 1 minuto")
            time.sleep(60)

    elif((texto.__contains__("buscar en")) or (texto.__contains__("busca en"))):
        if ((texto.__contains__("google")) or (texto.__contains__("navegador"))):
            palabras = texto.split()
            contadorPalabras = len(palabras)
            if (contadorPalabras > 3):
                global validarBusquedaG 
                validarBusquedaG = True
                texto = texto.replace("buscar en google", "")
                global resultadosBusquedaG
                resultadosBusquedaG = search(texto , tld="com", lang="es", num=5,start=0, stop=5, pause=3.0 )
                hablar("He encontrado estas 5 páginas para ti, ¿Quieres que las abra?. Contesta con un: abrir páginas")
            else: 
                validarBusquedaG = False
                hablar("No me haz dicho que quieres que busque. Repítelo, por favor")
        return
    
    elif (texto.__contains__("abrir")):
        if (validarBusquedaG == True):
            if((texto.__contains__("paginas")) or (texto.__contains__("páginas")) or (texto.__contains__("página")) or (texto.__contains__("pagina")) or (texto.__contains__("sitios"))or (texto.__contains__("sitio"))or (texto.__contains__("sitios"))or (texto.__contains__("dominio"))or (texto.__contains__("dominios"))):
                for r in resultadosBusquedaG:
                    if (r == 1): 
                        webbrowser.open(r, new=1) 
                    else:
                        webbrowser.open_new_tab(r)
        else: 
            hablar("Primero tienes que decirme qué quieres buscar en el navegador")            
        return

    elif(texto.__contains__("crear")): 
        if(texto.__contains__("recordatorio")):
            hablar("Ok. Dime en que fecha quieres crear el recordatorio")
            global crearRecordatorio
            crearRecordatorio = True
        if(texto.__contains__("aviso")):
            hablar("Ok. Dime dentro de cuanto quieres que lo avise")
            global crearAviso 
            crearAviso = True
        return

    elif(crearRecordatorio == True):
        hoy = datetime.date.today() 
        try:
            if (texto.__contains__("hoy")):
                hablar(hoy)
                global fechaParaRecordar
                fechaParaRecordar = hoy.strftime('%Y-%m-%d')
            else: 
                dia = -1 
                mes = -1 
                fecha = texto
                fecha = fecha.replace("de", "")
                fecha = fecha.replace("del", "")
                if (fecha.__contains__("2020")):
                    año = 2020
                elif (fecha.__contains__("2021")):
                    año = 2021
                elif (fecha.__contains__("2022")):
                    año = 2022
                elif (fecha.__contains__("2023")): 
                    año = 2023
                else:
                    if (fecha.__contains__("2024")):
                        año = 2024
                for palabra in fecha.split():  
                    if palabra in MESES:
                        mes = MESES.index(palabra) +1 
                    else:
                        if palabra.isdigit():
                            diaOaño = int(palabra)
                            if diaOaño< 2000:
                                dia= int(palabra)
                fecha =datetime.date(month=mes, day=dia, year=año)
                hablar(fecha)
                fechaParaRecordar = fecha.strftime('%Y-%m-%d')
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


    elif (crearAviso == True):
        try:
            hora = 0
            minutos = 0
            prueba = texto 
            prueba = prueba.replace("dentro", "")
            prueba = prueba.replace("de", "")
            for palabra in prueba.split():
                    if palabra.isdigit():
                        MinOhora= int(palabra)
            if (prueba.__contains__("minutos")):
                minutos = MinOhora
            else: 
                if ((prueba.__contains__("horas")) or (prueba.__contains__("hora"))):
                    hora = MinOhora
            #COMPROBAR FUNCIONAMIENTO:
            horaDate = datetime.time(hora, minutos)
            print(horaDate)
            global horaParaRecordar
            horaParaRecordar = horaDate.strftime('%H:%M')
            #HASTA ACA NOSE SI ANDA
            hablar("Dime que quieres que te avise")
            global crearAvisoTexto 
            crearAvisoTexto = True
            crearAviso = False
        except:
            print(horaParaRecordar)
            hablar("Ingresaste una hora inválida, vuelve a intentarlo")
        return
    else: 
        if (crearAvisoTexto == True):
            hablar("Ok. Aviso creado")
            recordatoriosAvisos.creacionAviso(horaParaRecordar, texto)
            crearAvisoTexto = False
        
    


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