import streamlit as st
import requests
import json
from data_loader import load_data

API_ENDPOINT = st.secrets["MODEL_API"]

# page config
st.set_page_config(layout="wide")

# model
def predict(data_input):
    """
    Hace una solicitud POST a la API de FastAPI para obtener una predicción.

    Args:
        data_for_prediction (dict): Un diccionario con los datos de entrada para la predicción,
                                    con las claves que coinciden con el modelo Pydantic de FastAPI.

    Returns:
        float or None: El valor de la predicción si la solicitud es exitosa, de lo contrario None.
    """
    api_endpoint = f"{API_ENDPOINT}/predict/"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(api_endpoint, headers=headers, data=json.dumps(data_input))
        response.raise_for_status()  # Lanza una excepción para códigos de estado HTTP de error (4xx o 5xx)

        prediction_result = response.json()
        if "prediction" in prediction_result and isinstance(prediction_result["prediction"], list):
            # Tu API devuelve la predicción como una lista (ej. [valor]), toma el primer elemento
            return prediction_result["prediction"][0]
        else:
            st.error(f"Formato de respuesta inesperado de la API: {prediction_result}")
            return None
    except requests.exceptions.ConnectionError:
        st.error(f"No se pudo conectar con la API en {API_ENDPOINT}. ¿Está la API en ejecución?")
        return None
    except requests.exceptions.Timeout:
        st.error("La solicitud a la API excedió el tiempo de espera.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error al hacer la solicitud a la API: {e}")
        st.error(f"Respuesta de la API (si disponible): {response.text}")
        return None
    except json.JSONDecodeError:
        st.error("Error al decodificar la respuesta JSON de la API.")
        st.error(f"Respuesta cruda: {response.text}")
        return None



# data
table = load_data("./precio_casas_rm - precio_casas_rm.csv")

# tile
st.title("Precio de las Casas :blue[_Región Metropolitana de Chile_] 🆑")
st.write("Modelo de Regresión creando usando los datos de los Precios de las Casas Usadas en la Región Metropolitana de Chile.")

# links

st.link_button("Origen de los datos", "https://www.kaggle.com/datasets/luisfelipetn/valor-casas-usadas-chile-rm-08032023")
st.link_button("Código Fuente del Modelo en Colab", "https://colab.research.google.com/drive/1ToxpRRnyUK7xBUiOmT-XhmXe0aGjr5FJ?usp=sharing")

# section 1
st.header("Muestra de los datos", divider=True)
st.dataframe(table)

# modelo

st.header("Modelo de Predicción del Precio de las Casas Usadas en la RM, Chile 🆑", divider=True)

rooms = st.slider("Habitaciones", 1.0, 5.0, 2.0, step=1.0)
baths = st.slider("Baños", 1.0, 4.0, 2.0, step=1.0)
built_area = st.slider("Área Construida en M2", 1.0, 208.0, 2.0, step=1.0)
total_area = st.slider("Área Total en M2", 1.0, 480.0, 25.0, step=1.0)
parking = st.slider("Estacionamientos", 1.0, 3.0, 2.0, step=1.0)

st.write("Has seleccionado: ")
st.write(f"- Dormitorios: {rooms}")
st.write(f"- Baños: {baths}")
st.write(f"- Área Construida en M2: {built_area}")
st.write(f"- Área Total en M2: {total_area}")
st.write(f"- Estacionamientos:  {parking}")

# Botón para hacer la predicción
if st.button("Predecir Precio"):
    # Prepara los datos en el formato esperado por tu API de FastAPI
    input_data_for_api = {
        "dormitorios": rooms,
        "baños": baths,
        "area_construida": built_area,
        "area_total": total_area,
        "estacionamients": parking
    }

    with st.spinner("Realizando predicción..."):
        predicted_price = predict(input_data_for_api)

    if predicted_price is not None:
        st.success(f"El precio predicho de la casa es: **${predicted_price:,.2f}**")
    else:
        st.warning("No se pudo obtener una predicción. Por favor, revisa los errores anteriores.")