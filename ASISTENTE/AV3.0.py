from sys import int_info
import threading
from tkinter.constants import TOP
import speech_recognition as sr 
#De aca importo todas las acciones que puede llegar a realizar el bot
import accionesYhabla
import tkinter as tk


from threading import Thread

def iniciarAsistente():
    listener = sr.Recognizer()
    nombre = 'verónica'
    Llamado = False
    while True:
        try:
            with sr.Microphone() as source: 
                listener.adjust_for_ambient_noise(source, duration=1)
                voz = listener.listen(source)
                texto = listener.recognize_google(voz, language="es-ES")
                if Llamado == True: 
                    if ('gracias verónica' or 'gracia verónica' or 'gracia veronica' or 'gracias veronica' or 'gracias vero' or    'gracia vero' or 'gracias')  in texto.lower():
                        Llamado = False
                        accionesYhabla.hablar('De nada')
                        texto = ''
                        break
                    accionesYhabla.acciones(texto.lower())
                if nombre.lower() in texto.lower(): 
                    accionesYhabla.hablar("Si, ¿qué necesitas?")
                    Llamado = True
                texto= ''
        except sr.UnknownValueError:
            listener = sr.Recognizer()

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

ventana = tk.Tk()
ventana.title("Asistente Virtual")
ventana['bg'] = '#232528'
ventana.geometry("300x300")
ventana.resizable(0,0)
ventana.iconbitmap(r'ASISTENTE/veronica.ico')

botonIniciarAsistente = tk.Button(ventana, text= "Iniciar Asistente", command= AsistenteIniciado, padx=30, pady=20)
botonIniciarAsistente.pack(side=TOP)
botonIniciarAsistente['bg'] = '#EAF6FF'

info_label = tk.Label(text = "Asistente Inactivo")
info_label['bg'] = '#232528'
info_label['fg'] = '#EAF6FF'
info_label.pack(before=botonIniciarAsistente, pady=20)


ventana.mainloop()