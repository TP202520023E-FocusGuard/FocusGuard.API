import spacy
import unicodedata
import re
from spacy.lang.es.stop_words import STOP_WORDS


# Cargar modelo en español de SpaCy para lematización
nlp = spacy.load('es_core_news_sm')

# Función para eliminar acentos y pasar a minúsculas
def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto

# Crear lista de stopwords normalizada (sin acentos)
stopwords_normalizadas = set(normalizar_texto(palabra) for palabra in STOP_WORDS)


def preprocesar_texto(texto):
    # Eliminar URLs
    texto = texto = re.sub(r'http\S+|www\S+|https\S+', ' ', texto)

    # Normalizar texto (minúsculas y sin acentos)
    texto_norm = normalizar_texto(texto)

    # Eliminar puntuación y caracteres no alfabéticos (conservando espacios)
    texto_norm = re.sub(r'[^a-zA-Z\s]', ' ', texto_norm)

    # Tokenizar con spaCy (sin lematizar aquí para mantener la forma limpia)
    doc = nlp(texto_norm)

    # Filtrar tokens cuyo texto normalizado está en stopwords normalizadas
    tokens_filtrados = [token.text for token in doc if token.text not in stopwords_normalizadas and token.text.strip() != '']
    return ' '.join(tokens_filtrados)