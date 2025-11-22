from joblib import load
from preprocessing import preprocesar_texto


def obtener_predicciones(modelo_pipe, texto):

    texto_preprocesado = preprocesar_texto(texto)

    predicciones = modelo_pipe.predict([texto_preprocesado])

    # Probabilidad de cada clase
    probabilidades = modelo_pipe.predict_proba([texto_preprocesado])

    # Probabilidad de la clase positiva en clasificación binaria:
    prob_clase_positiva = probabilidades[:, 1]

    return predicciones[0], probabilidades[0]


if '__main__' == __name__:
    # Para cargar y usar luego:
    modelo_pipe = load('./models/modelo_tfidf_logreg.joblib')
    texto_prueba = 'La vacuna Sputnik V: por qué genera dudas la vacuna aprobada por Rusia contra el covid-19'
    prediccion, probabilidades = obtener_predicciones(modelo_pipe, texto_prueba)
    clases = ['No ocio', 'Ocio']
    print("Probabilidades")
    print(f"- No ocio: {probabilidades[0]:.3f}")
    print(f"- Ocio: {probabilidades[1]:.3f}")
    print(f'Predicción: {clases[prediccion]}')