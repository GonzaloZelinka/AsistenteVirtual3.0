import time 
import threading
from tkinter.constants import TOP
import speech_recognition as sr 
import tkinter as tk

detener = False

def iniciarAsistente():
    global detener
    while True: 
        if detener == True: 
            print('rompiendo hilo')
            break
        print('Probando')
        time.sleep(3)

#Funciones que permiten el uso de hilos para evitar cierres inoportunos con la GUI


def schedule_check(t): 
    print('Hilo: ', t.is_alive())
    ventana.after(1000,finalizo, t)

#FALTA VER COMO DETENER EL HILO, no estaria encontrando como
def finalizo(t): 
    print('Hilo: ', t.is_alive())
    if t.is_alive(): 
        print('Hilo vivo')
        botonTerminarAsistente['state'] = 'normal'
    if not t.is_alive() or detener == True: 
        print('Hilo muerto')
        #print('Hilo muerto: ', t.is_alive())
        info_label["text"] = "Asistente Inactivo"
        botonIniciarAsistente["state"] = "normal"
        botonTerminarAsistente["state"] = "disabled"
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
    print('Hilo: ', t.is_alive())
    schedule_check(t)

def terminarAsistente():
    botonTerminarAsistente["state"] = "disabled"
    print('Prueba de que se activa')
    global detener
    detener = True
    

if __name__ == '__main__':
    ventana = tk.Tk()
    ventana.title("Asistente Virtual")
    ventana['bg'] = '#232528'
    #ventana.geometry("500x300")
    ventana.resizable(0,0)
    ventana.iconbitmap(r'veronica.ico')
    
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


