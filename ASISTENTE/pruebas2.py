from logging import error
from tkinter.constants import FALSE
import stanza
import re 
from unicodedata import normalize
import pywhatkit
from selenium import webdriver
from googlesearch import search
import webbrowser

from stanza.resources.common import process_pipeline_parameters

existe_accion = False

palabras_exc = ['en', 'el', 'podrias', 'deberias', 'la', 'las', 'los', 'es', 'ahi', 'aquello', 'aquellos', 'aqui', 'tu', 'tus', 'un', 'unas', 'una', 'unos']
acciones_p = ['dia buen', 'dias buenas', 'tarde buena', 'noche buena', 'noches buenas', 'tardes buenas', 'ROOT hola', 'crear recordatorio', 'buscar google', 'reproducir youtube', 'reproduce youtube', ]
nlp = stanza.Pipeline(lang='es')
accion_list = list()
error = False
acciones_juntas = False
def s_tilde(texto):
    texto = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", texto), 0, re.I)
    texto = normalize( 'NFC', texto)
    return texto



def acciones_IA(texto):
    global palabras_exc
    global crearRecordatorio
    global crearTextoRecordatorio
    global acciones_p
    global error
    global existe_accion

    existe_accion = False
    texto = s_tilde(texto)
    doc = nlp(texto)
    doc.sentences[0].print_dependencies()
    for sent in doc.sentences:
        for dep in sent.dependencies: 
            if dep[2].text:
                accion_list.append(dep[2].text)
    for sent in doc.sentences:
        for dep in sent.dependencies:
            if dep[2].text not in palabras_exc:
                accion = dep[0].text + ' ' + dep[2].text
                print('ACCIONES: ',accion)
                if accion in acciones_p:
                    print('ENCONTRO ESTA ACCION:', accion)
                    existe_accion = True
                    acciones(accion=accion, texto=texto, accion_list=accion_list) 
    if existe_accion == False:
        acciones_sIA(texto=texto, accion_list=accion_list)
        if error == True: 
            error = False
            return
    if existe_accion == True:
        for sent in doc.sentences:
            for dep in sent.dependencies:
                if dep[2].text not in palabras_exc:
                    #print(dep[0].text, dep[2].text) 
                    accion = dep[0].text + ' ' + dep[2].text
                    acciones(accion=accion, texto=texto, accion_list=accion_list) 

browser = webdriver

def busqueda_sIA(texto, accion_list, parar,parar_2, p_busqueda, e_busqueda): 
    i = 0 
    print(accion_list)
    print(texto)
    busqueda = ' '
    llego = False
    if e_busqueda not in texto: 
        pos = accion_list.index(p_busqueda)
        accion_list.insert(pos, 'en')
        print(accion_list)
    try: 
        for accion in accion_list: 
            if llego == True: 
                if len(accion_list) > (i+1):
                    if accion_list[i+1] != p_busqueda: 
                        busqueda = busqueda + ' ' + accion
            if accion == parar or accion == parar_2: 
                if accion_list[i+2] == p_busqueda:
                    print('No comprendi lo que me solicitó, vuelva a intentarlo porfavor')
                    #probar si esto permite reiniciar la escucha por si hubo algun error cuando se definio alguna accion. 
                    error = True
                    break
                else: 
                    if accion_list[i+1] != p_busqueda:
                       llego = True
            i += 1
    except: 
        print('No comprendi lo que me solicitó, vuelva a intentarlo porfavor')
        error = True
        return error
    return busqueda

#Habria que probar
def acciones_sIA(texto,accion_list): 
    global error
    global acciones_juntas
    #FIJARSE COMO TRAER PARAMETROS OPCIONALES
    if acciones_juntas == True: 
        busq_list = accion_list

        #FUNCIONA PERFECTO. SIRVE PARA CUANDO ME PIDE VARIAS ACCIONES, tipo buscar un youtube algo y en google a la vez
        if 'en youtube' in texto or 'youtube' in texto: 
            i = 0
            while True: 
                acciones = accion_list[i]
                i += 1 
                if acciones == 'reproduce' or acciones == 'reproducir': 
                    i = 0 
                    busq_list.pop(0)
                    if 'en youtube' not in texto: 
                        pos = accion_list.index('youtube')
                        accion_list.insert(pos, 'en')
                        print(accion_list)
                    for acciones in busq_list:
                        if busq_list[i+2] == 'youtube' or acciones == 'youtube':
                            busq_list.pop(i+2)
                            busq_list.pop(i+1)
                            romper = True 
                            break
                    if romper == True:
                        break
                    else: 
                        busq_list.pop(0)
                        i = 0
            print('Lista final:', busq_list)
            busq = str(busq_list)
            print('lo que se va a buscar: ',busq)
    # NO SIEMPRE TIENE QUE VENIR DOS ACCIONES        
    else:
        if 'en youtube' in texto or 'youtube' in texto: 
            busqueda = busqueda_sIA(texto, accion_list, 'reproduce', 'reproducir', 'youtube', 'en   youtube')
            print('busqueda yb: ',busqueda)
            busqueda = ''
        if 'en google' in texto or 'google' in texto:
            busqueda = busqueda_sIA(texto,accion_list, 'buscar', 'buscame','google', 'en google')
            print('busqueda go: ',busqueda)
            busqueda = ''
        else: 
            if busqueda == True: 
                error = True
                return 

def acciones(accion, texto, accion_list): 
    global existe_accion
    global acciones_juntas
    i = 0
    existe_accion = False
    esc = False
    romper = False
    #SIRVE PARA CUANDO VIENE UNA SOLA ACCION DEL TIPO 'buscar en youtube...'
    if 'reproduce youtube' in accion or 'reproducir youtube' in accion:
        busq_list = accion_list
        #ACA COMPRUEBO QUE SEA JUSTAMENTE UNA SOLA ACCION, ya que a veces si son varias se puede obtener el reproduce youtube como token
        while True:
            acciones = accion_list[i]
            i += 1
            print('VA EN: ',acciones)
            if acciones == 'reproduce' or acciones == 'reproducir': 
                print('Entro0')
                i = 0
                for acciones in busq_list:
                    if busq_list[i+2] == 'youtube': 
                        existe_accion = True
                        romper = True
                        break 
                    if acciones == 'youtube': 
                        print('Entro1')
                        acciones_juntas = True
                        existe_accion = False
                        romper = True
                        print(existe_accion)
                        break
            if romper == True: 
                break
            else: 
                print('borrando: ',busq_list.pop(0))
                i = 0
                #busq_list.pop(i)
        print(busq_list)
        if existe_accion == False:
            return
        # SI EXISTE BIEN LA ACCION, osea es solo esa y esta bien escrita, hago la busqueda como siempre
        if existe_accion == True: 
            busq_list = accion_list
            while True:
                if 'youtube' in busq_list[0]:
                    busq_list.pop(0)
                    #print('Se borro: ', busq_list[0])
                    break
                else: 
                    #print('Se borro: ', busq_list[0])
                    busq_list.pop(0)
            busqueda = str(busq_list)
            print("Ok, abriendo Youtube y Reproduciendo" + busqueda)
            pywhatkit.playonyt(busqueda)
            return
    # TODAVIA SIN ARREGLAR
    if 'buscar google' in accion:
        for acciones in accion_list:
            if acciones == 'buscar' or acciones == 'buscame': 
                if accion_list[i+2] == 'youtube': 
                    acciones_sIA(texto,accion_list)
                    esc = True
                    break
                else: 
                    break
        if esc == True:
            esc = False
            return
        print('Ok, realizando búsqueda')
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
        print("Búsqueda finalizada, abriendo páginas")
        num = 0
        for r in resultadosBusquedaG: 
            if num <= 5:
                if 'https://es.wikipedia.org/' in r or 'https://www.youtube.com/' in r or 'https://listado.mercadolibre.com.ar/' in r or 'https://www.mercadolibre.com.ar/' in r or 'https://www.cotodigital3.com.ar/' in r or 'https://www.manfrey.com.ar/' in r: 
                    if num != 0:
                        num -= 1
                else: 
                    webbrowser.open(r, new=2)
        return

acciones_IA('buscar hola soy german en google y reproduce zabatum en youtube')

#verónica quiero reproducir hola soy german en youtube // 
#('verónica', 2, 'amod')
#('quiero', 6, 'csubj')
#('reproducir', 2, 'xcomp')
#('hola', 3, 'obj')
#('soy', 6, 'cop')
#('german', 0, 'root')
#('en', 8, 'case')
#('youtube', 6, 'nmod')
#quiero verónica
#german quiero
#quiero reproducir
#reproducir hola
#german soy
#ROOT german
#youtube en
#german youtube

#verónica quiero reproducir en youtube hola soy german //
#('veronica', 2, 'amod')
#('quiero', 0, 'root')
#('reproducir', 2, 'xcomp')
#('en', 5, 'case')
#('youtube', 3, 'obl')
#('hola', 8, 'nsubj')
#('soy', 8, 'cop')
#('german', 2, 'ccomp')
#quiero veronica
#ROOT quiero
#quiero reproducir
# \\reproducir youtube\\
#german hola
#german soy
#quiero german

