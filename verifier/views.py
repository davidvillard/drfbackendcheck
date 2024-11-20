from .models import Url, Email, Phone, Sms
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import UrlSerializer, EmailSerializer, PhoneSerializer, SmsSerializer
from .validators import verify_url, verify_email, verify_phone, verify_sms


class UrlViewSet(viewsets.ModelViewSet):
    queryset = Url.objects.all()  # Indica los datos con los que va a trabajar la vista
    # Define que serializador se va a usar en la vista
    serializer_class = UrlSerializer

    # Definimos los metodos que se van a usar en la vista
    @action(detail=False, methods=['post', 'get'])
    def validate(self, request):
        # Recojemos la URL que el usuario envia
        user_url = request.data.get('nombre_url')
        if not user_url:
            return Response({"error": "La URL es obligatoria"}, status=400)

        url_obj = Url.objects.filter(nombre_url=user_url).first()
        if url_obj:
            return Response({
                'message': url_obj.message  # Esto muestra un texto diciendo si la url es valida o no
            })

        validation_message = verify_url(request, user_url)
        print(f"Mensaje validacion: {validation_message}")

        # Verificar si el mensaje indica un error
        if "Error" in validation_message or "Límite" in validation_message:
            status_message = validation_message
            is_valid = False

            return Response({
                status_message
            })
        else:
            is_valid = "La URL es segura" in validation_message
            status_message = validation_message if is_valid else "La URL no es segura"

            url_obj = Url.objects.create(
                nombre_url=user_url,
                is_valid=is_valid,
                message=status_message
            )

            return Response({
                url_obj.message  # Esto muestra un texto diciendo si la url es valida o no
            })

class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer

    @action(detail=False, methods=['post', 'get'])
    def validate(self, request):
        user_email = request.data.get("email")
        if not user_email:
            return Response({"error": "El email es obligatorio"}, status=400)

        email_obj = Email.objects.filter(email=user_email).first()
        if email_obj:
            return Response({
                # Esto deberia mostrar un texto diciendo si la url es valida o no
                'message': email_obj.message
            })

        validation_message = verify_email(request, user_email)

        if "Error" or "Limite" or "Ha" in validation_message:
            status_message = validation_message
            is_valid = False

            return Response({
                status_message  # Esto deberia mostrar un texto diciendo si la url es valida o no
            })
        else:
            is_valid = "El email es seguro" in validation_message
            status_message = validation_message if is_valid else "El email no es seguro"

            email_obj = Email.objects.create(
                email=user_email,
                is_valid=is_valid,
                message=status_message
            )

            return Response({
                email_obj.message  # Esto deberia mostrar un texto diciendo si la url es valida o no
            })

class PhoneViewSet(viewsets.ModelViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer

    @action(detail=False, methods=['post', 'get'])
    def validate(self, request):
        user_number = request.data.get("phone")
        if not user_number:
            return Response({"error": "El número de teléfono es obligatorio"}, status=400)

        phone_obj = Phone.objects.filter(phone=user_number).first()
        if phone_obj:
            return Response({
                # Esto deberia mostrar un texto diciendo si la url es valida o no
                'message': phone_obj.message
            })

        validation_message = verify_phone(request, user_number)

        if "Error" or "Limite" or "Ha" in validation_message:
            status_message = validation_message
            is_valid = False

            return Response({
                status_message  # Esto deberia mostrar un texto diciendo si la url es valida o no
            })
        else:
            is_valid = "El telefono es seguro" in validation_message
            status_message = validation_message if is_valid else "El telefono no es seguro"

            phone_obj = Phone.objects.create(
                phone=user_number,
                is_valid=is_valid,
                message=status_message
            )

            return Response({
                phone_obj.message  # Esto deberia mostrar un texto diciendo si la url es valida o no
            })

class SmsViewSet(viewsets.ModelViewSet):
    queryset = Sms.objects.all()
    serializer_class = SmsSerializer

    @action(detail=False, methods=['post', 'get'])
    def validate(self, request):
        message_sms = request.data.get("message_sms")
        if not message_sms:
            return Response({"error": "El Sms es obligatorio"}, status=400)

        sms_obj = Sms.objects.filter(message_sms=message_sms).first()
        if sms_obj:
            return Response({
                # Esto deberia mostrar un texto diciendo si la url es valida o no
                'message': sms_obj.message
            })

        validation_message, valido = verify_sms(request, message_sms)

        # Inicializar is_valid y status_message con valores predeterminados
        is_valid = valido  # Asume que es inseguro por defecto
        status_message = validation_message

        sms_obj = Sms.objects.create(
            message_sms=message_sms,
            is_valid=is_valid,
            message=status_message
        )

        return Response({
            sms_obj.message  # Esto deberia mostrar un texto diciendo si la url es valida o no
        })
