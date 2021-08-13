import os
from time import sleep
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy
import sys
import webbrowser
import pyautogui
from time import sleep
import json
bandera = False
load_dotenv()
ID_SPOTIFY = os.getenv("ID_SPOTIFY")
ID_SPOSECRET = os.getenv("ID_SPOSECRET")
SPOTIFY_URI = os.getenv("SPOTIFY_URI")

#esto funciona con una sola cancion
#autor = ''
#cancion_b = 'bad guy'.lower()
#esto funciona con una sola cancion
#if len(autor) > 0:
#    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(ID_SPOTIFY, ID_SPOSECRET))
#    resultado = sp.search(autor)
#    for i in range(0, len(resultado['tracks']['items'])):
#        cancion = resultado['tracks']['items'][i]['name'].lower()
#        if cancion in cancion_b: 
#            bandera = True
#            webbrowser.open(resultado['tracks']['items'][i]['uri'])
#
#if bandera == False: 
#    cancion_b = cancion_b.replace(" ", "%20")
#    webbrowser.open(f'spotify:search:{cancion_b}')
#    sleep(5)
#    for i in range(30):
#        pyautogui.press("tab")
#        #sleep(1)
#    pyautogui.press("enter")
#

#tratando de que funcione con playlists

#Funciona pero solo si se spotify pasa a ser la app usada, para poder poner los comandos. Ya que pyautogui solo emula las teclas.
client_credentials_manager = SpotifyClientCredentials(ID_SPOTIFY, ID_SPOSECRET)
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(ID_SPOTIFY, ID_SPOSECRET))
#print(resultado)
resultado = sp.playlist("53zjvfwOfcktTLwbW9wvID")
#for i in range(0, len(resultado['items'])):
#    cancion = resultado['items'][i]['track']['uri']
#    duracion = resultado['items'][i]['track']['duration_ms']
#    
#
#    cancion = ''
#    duracion = 0
#    print(cancion)
#    print(duracion/1000)
webbrowser.open(resultado['uri'])
sleep(5)
b = True
if b == True:
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    b = False
