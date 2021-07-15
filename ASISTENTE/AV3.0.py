import speech_recognition as sr 
#De aca importo todas las acciones que puede llegar a realizar el bot
import accionesYhabla


listener = sr.Recognizer()
nombre = 'verónica'
Llamado = False
while True:
    try:
        with sr.Microphone() as source: 
            print('Escuchando...')
            listener.adjust_for_ambient_noise(source, duration=1)
            voz = listener.listen(source)
            texto = listener.recognize_google(voz, language="es-ES")
            if Llamado == True: 
                if (('gracias verónica' or 'gracia verónica' or 'gracia veronica' or 'gracias veronica' or 'gracias vero' or 'gracia vero' or 'gracias')).lower()  in texto.lower():
                    print('Desactivando...')
                    Llamado = False
                    accionesYhabla.hablar('De nada')
                    texto = ''
                accionesYhabla.acciones(texto.lower())
            if nombre.lower() in texto.lower(): 
                print('Activando...')
                accionesYhabla.hablar("Si, ¿qué necesitas?")
                Llamado = True
            print(texto)
            texto= ''
    except sr.UnknownValueError:
        print("Error...")
        listener = sr.Recognizer()
