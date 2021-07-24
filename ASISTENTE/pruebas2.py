import stanza
import re 
from unicodedata import normalize

palabras_exc = ['en', 'el', 'podrias', 'deberias', 'la', 'las', 'los', 'es', 'ahi', 'aquello', 'aquellos', 'aqui', 'tu', 'tus', 'un', 'unas', 'una', 'unos']
nlp = stanza.Pipeline(lang='es')
accion_list = list()
def s_tilde(texto):
    texto = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", texto), 0, re.I)
    texto = normalize( 'NFC', texto)
    return texto

def acciones_IA(texto):
    global palabras_exc
    global crearRecordatorio
    global crearTextoRecordatorio

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
                print(dep[0].text, dep[2].text)  

acciones_IA('buscar en google queso')