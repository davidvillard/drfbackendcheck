# Verificador de Seguridad

Este es un proyecto de Django que utiliza Django REST Framework para proporcionar una API que verifica la seguridad de URLs, correos electrónicos, números de teléfono y mensajes SMS. El proyecto está configurado para ser desplegado en Render.

## Estructura del Proyecto

```
└── 📁drf
    └── 📁drf
        └── 📁__pycache__
        └── __init__.py
        └── asgi.py
        └── settings.py
        └── urls.py
        └── wsgi.py
    └── 📁verifier
        └── 📁__pycache__
        └── 📁migrations
        └── __init__.py
        └── admin.py
        └── apps.py
        └── models.py
        └── serializers.py
        └── tests.py
        └── urls.py
        └── validators.py
        └── views.py
    └── .gitignore
    └── build.sh
    └── docker-compose.yml
    └── Dockerfile
    └── manage.py
    └── readme.md
    └── requirements.txt
```

## Requisitos

- Python 3.12.7
- Django 5.1.3
- Django REST Framework 3.15.2
- Render para despliegue

## Instalación

1. Clona el repositorio:

    ```sh
    git clone https://github.com/tu-usuario/verificador-seguridad.git
    ```

2. Instala las dependencias:

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


Límites y Códigos de Error de las APIs

| **API**          | **Límite de Llamadas**                                                                                   | **Códigos de Error**                                                                                                                                                                                                                                   |
|-------------------|---------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Phone**         | Entre 10 y 50 solicitudes por día, renovadas cada 24 horas.                                             | - **200**: Llamada exitosa.<br>- **400**: Error en la solicitud a la API.<br>- **2**: Límite de llamadas excedido.                                                                                                                                    |
| **Email**         | Entre 10 y 50 solicitudes por día, renovadas cada 24 horas.                                             | - **200**: Llamada exitosa.<br>- **400**: Error en la solicitud a la API.<br>- **2**: Límite de llamadas excedido.                                                                                                                                    |
| **URLs (VirusTotal)** | 500 solicitudes por día (renovadas a las 00:00). Máximo de 4 solicitudes por minuto.                  | - **200**: Llamada exitosa.<br>- **400**: Error en la solicitud a la API.<br>- **429**: Límite de llamadas excedido.                                                                                                                                  |
| **SMS**           | Sin límite de llamadas.                                                                                 | No aplica.                                                                                                                                                                                                                                           |

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.