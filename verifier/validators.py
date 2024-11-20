from django.shortcuts import render
from django.http import JsonResponse
import requests
import os
import string
from dotenv import load_dotenv

load_dotenv()


def verify_url(request, user_url):

    # Endpoint de VirusTotal para analizar la URL
    url = os.getenv("VIRUSTOTAL_URL_VERIFY")
    payload = {"url": user_url}  # Parametro que le paso a la API
    headers = {
        "accept": "application/json",
        "x-apikey": os.getenv("VIRUSTOTAL_API_KEY"),
        "content-type": "application/x-www-form-urlencoded"
    }

    # Realizar la solicitud a VirusTotal
    # Hago la solicitud POST a la API
    response = requests.post(url, data=payload, headers=headers)

    status_message = ""
    error_messages = {
        400: "Error en la solicitud",
        429: "Limite de llamadas a la API alcanzado"
    }

    # Si el status code es 400 o 429, muestro el mensaje de error
    status_message = error_messages.get(response.status_code)

    # Extraer el ID de análisis del resultado de VirusTotal
    response_data = response.json()  # Extraigo el JSON de la respuesta
    analysis_id = response_data.get("data", {}).get(
        "id")  # Recojo el id para analizarlo

    if not analysis_id:
        status_message = "No se pudo obtener el ID de analisis"

    # Llamar a la función de análisis con el ID
    # Llamo a la funcion de analisis pasandole el id para saber si es segura la url o no
    return analyse_url(analysis_id, status_message)


def analyse_url(analysis_id, status_message):
    # Construir la URL con el ID del análisis
    # El id se le pasa como parametro a la URL
    url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    headers = {
        "accept": "application/json",
        "x-apikey": os.getenv("VIRUSTOTAL_API_KEY")
    }

    # Realizar la solicitud GET para obtener el análisis
    # Hago la solicitud get a la API
    response = requests.get(url, headers=headers)
    print(f"Respuesta del análisis: {response.status_code}, {
          response.text}")  # Ver la respuesta completa

    error_messages = {
        400: "Error en la solicitud",
        429: "Limite de llamadas a la API alcanzado"
    }

    # Si el status code es 400 o 429, muestro el mensaje de error
    status_message = error_messages.get(response.status_code)
    print(f"Mensaje de error: {status_message}")  # Ver el mensaje de error

    if response.status_code == 200:
        message_data = {  # Creo un diccionario con los datos que me interesa utilizar ( en este caso verificar cuantos maliciosos hay)
            'message': status_message
        }

        malicious_count = response.json().get('data', {}).get('attributes', {}).get('stats', {}).get(
            'malicious')  # Cuento que numero de antivirus detectaron la url como maliciosa
        # Ver el numero de antivirus que detectaron la url como maliciosa
        print(f"Numero de antivirus que detectaron la URL como maliciosa: {
              malicious_count}")
        # Determino si la URL es segura o maliciosa
        status_message = "La URL es segura" if malicious_count == 0 else "La URL no es segura"

        # Incluyo el mensaje en la respuesta
        message_data['message'] = status_message
        print(f"Mensaje: {status_message}")
    return status_message  # Devuelvo el mensaje de si la url es segura o no


def verify_email(request, user_email):

    url = os.getenv("NEUTRINO_EMAIL")  # URL de la API
    headers = {
        "User-ID": os.getenv("NEUTRINO_USER_ID"),
        "API-Key": os.getenv("NEUTRINO_API_KEY"),
    }
    # Parametros que le paso a la api
    payload = {"email": user_email, "fix-typos": "false"}

    # Hago la solicitud POST a la API
    response = requests.post(url, headers=headers, data=payload)
    print(f"Respuesta de la API: {response.status_code}, {
          response.text}")  # Muestra la respuesta de la API

    response_data = response.json()  # Recojo el JSON de la respuesta
    # Recojo el valor de valid dentro del JSON
    valid = response_data.get('valid')
    # Recojo el valor de smtp-status dentro del JSON
    smtp_status = response_data.get('smtp-status')
    # Recojo el valor de domain dentro del JSON
    email = response_data.get('email')
    # Muestra los valores de 'smtp-status' y 'valid'
    print(f"Estado del SMTP: {smtp_status}, Validación: {valid}")

    if response.status_code != 200:
        api_error = response_data.get('api-error')
        # Si el status code no es 200, muestro el mensaje de error
        status_message = "Limite de llamadas a la API alcanzado" if api_error == 2 else "Error en la solicitud a la API"
        print(f"Mensaje de error: {status_message}, api-error: {api_error}")  # Muestra el mensaje de error
        
        response_data['message'] = status_message  # Añado el mensaje al JSON
        # Muestra los valores de 'smtp-status' y 'valid'
        print(f"Mensaje: {status_message}")

        return status_message  # Devuelvo el mensaje diciendo si el email es seguro o no
    
    else:
        
        if smtp_status == "invalid" or valid == False:
            status_message = "El email no es seguro"
        else:
            status_message = "El email es seguro" if smtp_status == "ok" and valid == True else "El email no es seguro"

        status_message = "Ha ocurrido un error y no se ha podido verificar el email" if '@' not in email else status_message

        response_data['message'] = status_message  # Añado el mensaje al JSON
        # Muestra los valores de 'smtp-status' y 'valid'
        print(f"Mensaje: {status_message}")

        return status_message  # Devuelvo el mensaje diciendo si el email es seguro o no


def verify_phone(request, user_number):
    url = os.getenv("NEUTRINO_PHONE")  # URL de la API
    headers = {
        'User-ID': os.getenv("NEUTRINO_USER_ID"),
        'API-Key': os.getenv("NEUTRINO_API_KEY"),
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload = {  # Parametros que le pasamos a la API
        'number': user_number,
        'country-code': '',
        'ip': '',
    }

    response = requests.post(url, headers=headers, data=payload)
    print(f"Respuesta de la API: {response.status_code}, {
          response.text}")  # Muestra la respuesta de la API

    response_data = response.json()
    valid = response_data.get('valid')
    api_error = response_data.get('api-error')
    international_number = response_data.get('international-number')
    print(f"Numero internacional: {international_number}, Validación: {valid}, Api_Error: {api_error}")  # Muestra los valores de 'smtp-status' y 'valid'

    if response.status_code != 200:
        if api_error == 2:
            status_message = "Limite de llamadas a la API alcanzado"
        else:
            status_message = "Error en la solicitud a la API"

    if valid == True and international_number != "":
        status_message = "El telefono es seguro"
    elif valid == False and international_number != "":
        status_message = "El telefono no es seguro"
    elif valid == False and international_number == "":
        status_message = "Ha ocurrido un error y no se ha podido verificar el número de teléfono"

    response_data['message'] = status_message
    # Muestra los valores de 'smtp-status' y 'valid'
    print(f"Mensaje: {status_message}")
    return status_message


def verify_sms(request, message_sms):
    encontradas = False  # Boolenao que es True si encuentra palabras sospechosas
    # Mensaje que se mostrara como respuesta de si el sms es seguro o no (se añade a la base de datos)
    status_message = ""
    # Booleano que es True si el sms es seguro (se añade a la base de datos)
    valido = False
    suspicious_words = {'gratis', 'ganaste', 'premio', 'oferta', 'cuenta', 'pago',
                        'urgente', 'reembolso', 'reclamarlo', 'dinero', 'paga'}  # Palabras sospechosas

    # Buscar la posición de la URL
    http_position = message_sms.lower().find(
        "http")  # Busca en el mensaje la palabra http

    if http_position != -1:  # Si se encuentra http
        # Buscamos la posición final de la URL (hasta que encuentre un espacio)
        posicion_final = message_sms.find(" ", http_position)
        if posicion_final == -1:  # Si no encuentra un espacio, entonces la URL es la última palabra
            # Obtiene la URL hasta el final de la frase y quitamos espacios vacios
            presunta_url = message_sms[http_position:].strip()
        else:  # Si encuentra un espacio
            # Obtiene la URL hasta el espacio encontrado y quitamos espacios vacios
            presunta_url = message_sms[http_position:posicion_final].strip()

        # Coger el mensaje antes de http y quitarle los espacios vacios
        message_partition = message_sms.partition("http")[0].strip()
    else:  # Si no encuentra http
        presunta_url = ""  # No hay URL
        # Recogemos el mensaje en una variable para dividirla en palabras y buscar las sospechosas
        message_partition = message_sms

    # Limpio el mensaje quitandole los signos de puntuacion y pasandolo a minusculas (con maketrans creo como un diccionario de los signos de puntuacion a eliminar, y transalte lo que hace es eliminarlos de la frase cuando los encuentra)
    message_sms_clean = message_partition.translate(
        str.maketrans('', '', string.punctuation)).lower()

    message_words = message_sms_clean.split()  # Dividimos el mensaje en palabras

    # Verificar si alguna palabra es sospechosa
    for palabra in message_words:  # Por cada palabra en el mensaje
        if palabra in suspicious_words:  # Si la palabra esta en la lista de palabras sospechosas
            encontradas = True  # Cambiamos el valor de encontradas a True
            break  # No es necesario seguir buscando si ya encontramos una palabra sospechosa

    # Si encontramos palabras sospechosas y hay una URL
    if encontradas and presunta_url:
        # Recogemos el mensaje de la funcion de validacion de la url
        url_validation_message = verify_url(request, presunta_url)
        # Si el mensaje es que la url es segura
        url_message = "la url es segura" in url_validation_message.lower()

        if url_message:  # Si la url es segura
            status_message = "Sms sospechoso"
            valido = False
        elif not url_message:  # Si la url no es segura
            status_message = "Sms fraudulento"
            valido = False
        return status_message, valido  # Retornamos el mensaje y si es valido o no

    # Si no hay palabras sospechosas pero hay URL
    elif not encontradas and presunta_url:
        # Recogemos el mensaje de la funcion de validacion de la url
        url_validation_message = verify_url(request, presunta_url)
        # Si el mensaje es que la url es segura
        url_message = "la url es segura" in url_validation_message.lower()

        if url_message:  # Si la url es segura
            status_message = "Sms seguro"
            valido = True
        else:  # Si la url no es segura
            status_message = "Sms fraudulento"
            valido = False
        return status_message, valido  # Retornamos el mensaje y si es valido o no

    # Si no se encuentra ninguna palabra sospechosa ni URL
    if not encontradas:
        status_message = "Sms seguro (final)"
        valido = True
    else:  # Si se encuentra palabra sospechosa pero no hay URL
        status_message = "Sms sospechoso"
        valido = False

    return status_message, valido  # Retornamos el mensaje y si es valido o no
