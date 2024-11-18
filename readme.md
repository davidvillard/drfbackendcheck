# Verificador de Seguridad

Este es un proyecto de Django que utiliza Django REST Framework para proporcionar una API que verifica la seguridad de URLs, correos electrónicos, números de teléfono y mensajes SMS. El proyecto está configurado para ser desplegado en Render.

## Estructura del Proyecto

.env .gitignore build.sh db.sqlite3 docker-compose.yml Dockerfile drf/ init.py asgi.py settings.py urls.py wsgi.py manage.py requirements.txt verifier/ init.py admin.py apps.py migrations/ models.py serializers.py tests.py urls.py validators.py views.py


## Requisitos

- Python 3.12.7
- Django 5.1.3
- Django REST Framework 3.15.2
- Render para despliegue

## Instalación

1. Clona el repositorio:

    ```sh
    git clone https://github.com/tu-usuario/verificador-seguridad.git
    cd verificador-seguridad
    ```

2. Crea y activa un entorno virtual:

    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:

    ```sh
    pip install -r requirements.txt
    ```

4. Configura las variables de entorno en un archivo `.env`:

    ```env
    VIRUSTOTAL_API_KEY=tu_api_key
    VIRUSTOTAL_URL_VERIFY=https://www.virustotal.com/api/v3/urls
    NEUTRINO_EMAIL=https://neutrinoapi.net/email-verify
    NEUTRINO_PHONE=https://neutrinoapi.net/phone-validate
    NEUTRINO_API_KEY=tu_api_key
    NEUTRINO_USER_ID=tu_usuario
    SECRET_KEY_SETTINGS=tu_secret_key
    ```

5. Realiza las migraciones de la base de datos:

    ```sh
    python manage.py migrate
    ```

6. Ejecuta el servidor de desarrollo:

    ```sh
    python manage.py runserver
    ```

## Despliegue en Render

1. Crea una cuenta en [Render](https://render.com/).

2. Crea un nuevo servicio web y conecta tu repositorio de GitHub.

3. Configura las variables de entorno en Render usando los valores de tu archivo `.env`.

4. Render ejecutará automáticamente el archivo `build.sh` para instalar las dependencias y realizar las migraciones.

5. Una vez desplegado, tu API estará disponible en la URL proporcionada por Render.

## Uso de la API

La API proporciona los siguientes endpoints:

- `POST /api/verifier/url/validate/` - Valida una URL.
- `POST /api/verifier/email/validate/` - Valida un correo electrónico.
- `POST /api/verifier/phone/validate/` - Valida un número de teléfono.
- `POST /api/verifier/sms/validate/` - Valida un mensaje SMS.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.