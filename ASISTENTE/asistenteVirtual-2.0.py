
import speech_recognition as sr 
#De aca importo todas las acciones que puede llegar a realizar el bot
import accionesYhabla


listener = sr.Recognizer()
nombre = 'verónica'
Llamado = False

#Con este asistente controlo cuando debe escucharme y cuando no. Osea, cuando lo llame por su nombre.
def iniciarAsistente():
    try:  
        with sr.Microphone() as source: 
            voz = listener.listen(source)
            rec = listener.recognize_google(voz, language="es-ES")
            texto = str(rec).lower()
            if nombre in texto:
                print("Llamando a Verónica")
                print(texto)
                accionesYhabla.hablar("Si, ¿qué necesitas?")
                global Llamado
                Llamado = True
                texto= " "          
    except:
        pass
    return

#Con este asistente en cambio controlo los pedidos que puede realizar una persona, luego de haber invocado al asistente por su nombre.
def asistenteIniciado():
    try:  
        with sr.Microphone() as source: 
            voz = listener.listen(source)
            rec = listener.recognize_google(voz, language="es-ES")
            texto = str(rec).lower()
            print(texto)
            if((texto.__contains__("gracias verónica")) or (texto.__contains__("gracia verónica")) or (texto.__contains__("gracia veronica")) or (texto.__contains__("gracias veronica"))):
                global Llamado
                Llamado = False
                accionesYhabla.hablar("De nada")
                return
            accionesYhabla.acciones(texto) 
    except:
        pass
    return

#Ciclo donde sucede la magia
while True:
    if (Llamado == False): 
        iniciarAsistente()
    else:
        if (Llamado == True ): 
            asistenteIniciado()
    

