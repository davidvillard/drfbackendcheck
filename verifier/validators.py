import requests
import os
import json
import string
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from dotenv import load_dotenv
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import permission_classes, authentication_classes

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


@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def verify_phone(request, user_number):
     url = os.getenv("NEUTRINO_PHONE")

     response_data = {
         'api-error': 2,
         'valid': None,
         'international-number': None,
     }
     
     if response_data.get('api-error') == 2:
         status_message = "Limite de llamadas a la API alcanzado"
         print(f"Mensaje de error: {status_message}")

         user_email = request.user.email
         if not user_email:
             return Response({"message": "El usuario autenticado no tiene un email válido"}, status=400)

         # Lógica de verificación
         send_email(
             subject="Límite de API alcanzado",
             message="Se ha alcanzado el límite de llamadas a la API para la verificación de teléfonos.",
             to_email=user_email
         )
         return Response({"message": "Correo enviado correctamente"}, status=200)


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
        # Muestra el mensaje de error
        print(f"Mensaje de error: {status_message}, api-error: {api_error}")

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


# @authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])
# def verify_phone(request, user_number):
#     url = os.getenv("NEUTRINO_PHONE")  # URL de la API
#     headers = {
#         'User-ID': os.getenv("NEUTRINO_USER_ID"),
#         'API-Key': os.getenv("NEUTRINO_API_KEY"),
#         'Content-Type': 'application/x-www-form-urlencoded',
#     }
#     payload = {  # Parametros que le pasamos a la API
#         'number': user_number,
#         'country-code': '',
#         'ip': '',
#     }

#     response = requests.post(url, headers=headers, data=payload)
#     print(f"Respuesta de la API: {response.status_code}, {
#           response.text}")  # Muestra la respuesta de la API

#     response_data = response.json()
#     valid = response_data.get('valid')
#     international_number = response_data.get('international-number')
#     print(f"Numero internacional: {international_number}, Validación: {
#           valid}")  # Muestra los valores de 'smtp-status' y 'valid'

#     if response.status_code != 200:
#         api_error = response_data.get('api-error')
#         # Si el status code no es 200, muestro el mensaje de error
#         status_message = "Limite de llamadas a la API alcanzado" if api_error == 2 else "Error en la solicitud a la API"
#         # Muestra el mensaje de error
#         print(f"Mensaje de error: {status_message}, api-error: {api_error}")

#         response_data['message'] = status_message  # Añado el mensaje al JSON
#         print(f"Mensaje: {status_message}")

#         # Enviar el correo si el límite de llamadas ha sido alcanzado
#         if api_error == 2:
#             status_message = "Limite de llamadas a la API alcanzado"
#             print(f"Mensaje de error: {status_message}")

#             user_email = request.user.email
#             if not user_email:
#                 return Response({"message": "El usuario autenticado no tiene un email válido"}, status=400)

#             # Lógica de verificación
#             send_email(
#                 subject="Límite de API alcanzado",
#                 message="Se ha alcanzado el límite de llamadas a la API para la verificación de teléfonos.",
#                 to_email=user_email
#             )

#         return status_message  # Devuelvo el mensaje diciendo si el email es seguro o no
#     else:
#         if international_number:  # Las cadenas no vacias se evaluan como True
#             status_message = "El telefono es seguro" if valid else "El telefono no es seguro"
#         else:  # Las cadenas vacias se evaluan como False
#             status_message = "Ha ocurrido un error y no se ha podido verificar el número de teléfono" if not valid else "El telefono no es seguro"

#         response_data['message'] = status_message
#         # Muestra los valores de 'smtp-status' y 'valid'
#         print(f"Mensaje: {status_message}")
#         return status_message


def verify_sms(request, message_sms):
    # Definir palabras sospechosas
    suspicious_words = {'gratis', 'ganaste', 'premio', 'oferta', 'cuenta', 'pago',
                        'urgente', 'reembolso', 'reclamarlo', 'dinero', 'paga'}
    # Buscar URL en el mensaje
    http_position = message_sms.lower().find("http")
    presunta_url = message_sms[http_position:].split(
    )[0].strip() if http_position != -1 else ""

    # Limpiar y dividir el mensaje
    message_sms_clean = message_sms.translate(
        str.maketrans('', '', string.punctuation)).lower()
    message_words = message_sms_clean.split()

    # Verificar palabras sospechosas
    encontradas = any(word in suspicious_words for word in message_words)

    if presunta_url:
        url_validation_message = verify_url(request, presunta_url)
        url_message = "la url es segura" in url_validation_message.lower()
        # Satatus_message y is_valid van a coger el valor que le devuelva la funcion verify_status_sms: ("Sms fraudulento", False)...
        status_message, is_valid = verify_status_sms_with_url(
            encontradas, url_message)
    else:
        if encontradas:
            status_message = "Sms sospechoso"
            is_valid = False
        else:
            status_message = "Sms seguro (final)"
            is_valid = True

    print("Mensaje final:", status_message)
    print("Estado final (is_valid):", is_valid)

    return status_message, is_valid


def verify_status_sms_with_url(encontradas, url_message):
    estado = {
        (True, False): ("Sms fraudulento", False),
        (True, True): ("Sms sospechoso", False),
        (False, True): ("Sms seguro", True),
        (False, False): ("Sms fraudulento", False)
    }

    return estado[(encontradas, url_message)]


def send_email(subject, message, to_email):
    from_email = None
    send_mail(subject, message, from_email, [to_email])
