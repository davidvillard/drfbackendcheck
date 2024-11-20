from .models import Url, Email, Phone, Sms
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import UrlSerializer, EmailSerializer, PhoneSerializer, SmsSerializer
from .validators import verify_url, verify_email, verify_phone, verify_sms

class UrlViewSet(viewsets.ModelViewSet):
    queryset = Url.objects.all() # Indica los datos con los que va a trabajar la vista
    serializer_class = UrlSerializer # Define que serializador se va a usar en la vista
    @action(detail=False, methods=['post', 'get']) # Definimos los metodos que se van a usar en la vista
    def validate(self, request):
        user_url = request.data.get('nombre_url') # Recojemos la URL que el usuario envia
        if not user_url:
            return Response({"error": "La URL es obligatoria"}, status=400)
        
        url_obj = Url.objects.filter(nombre_url=user_url).first()
        if url_obj:
            return Response({
                'message' : url_obj.message # Esto muestra un texto diciendo si la url es valida o no
            })
            
        validation_message = verify_url(request, user_url)
        print(f"Mensaje de validación: {validation_message}")  # Ver lo que devuelve la función de validación
        
        is_valid = 'la url es segura' in validation_message.lower()
        if is_valid:
            status_message = "La URL es segura"
        else:
            status_message = "La URL no es segura"
        
        is_error = 'error en la solicitud' in validation_message.lower()
        if is_error:
            status_message = 'Ha ocurrido un error y no se ha podido verificar la URL'
            
        is_error_id = 'no se pudo obtener el id del analisis' in validation_message.lower()
        if is_error_id:
            status_message = 'Ha ocurrido un error y no se ha podido verificar la URL'
            
        is_error_limit = 'limite de llamadas a la api alcanzado' in validation_message.lower()
        if is_error_limit:
            status_message = 'Limite de llamadas a la API alcanzado'
            
            
        url_obj = Url.objects.create(
            nombre_url = user_url,
            is_valid = is_valid,
            message = status_message
        )
        
        return Response({
            url_obj.message #Esto muestra un texto diciendo si la url es valida o no
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
                'message' : email_obj.message #Esto deberia mostrar un texto diciendo si la url es valida o no
            })
            
        validation_message = verify_email(request, user_email)
        
        is_valid = 'el email es seguro' in validation_message.lower()
        # smtp_response = 'ha ocurrido un error y no se ha podido verificar el email' in validation_message.lower()
        
        if is_valid:
            status_message = "El email es seguro"
        else:
            status_message = "El email no es seguro"
        
        is_error = validation_message.lower()
        if is_error == "ha ocurrido un error y no se ha podido verificar el email":
            status_message = 'Ha ocurrido un error y no se ha podido verificar el email'
        elif is_error == "error en la solicitud a la API":
            status_message = 'Ha ocurrido un error con la solicitud a la API'
        elif is_error == "limite de llamadas a la api alcanzado":
            status_message = 'Limite de llamadas a la API alcanzado'
            
        email_obj = Email.objects.create(
            email = user_email,
            is_valid = is_valid,
            message = status_message
        )
        
        return Response({
            email_obj.message #Esto deberia mostrar un texto diciendo si la url es valida o no
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
                'message' : phone_obj.message #Esto deberia mostrar un texto diciendo si la url es valida o no
            })
            
        validation_message = verify_phone(request, user_number)
        
        is_valid = 'el telefono es seguro' in validation_message.lower()
        is_error = ""
        
        if is_valid:
            status_message = "El telefono es seguro"
        else:
            status_message = "El telefono no es seguro"
            
        is_error = validation_message.lower()
        if is_error == "ha ocurrido un error y no se ha podido verificar el número de teléfono":
            status_message = 'Ha ocurrido un error y no se ha podido verificar el número de teléfono'
        elif is_error == "error en la solicitud a la API":
            status_message = 'Ha ocurrido un error con la solicitud a la API'
        elif is_error == "limite de llamadas a la api alcanzado":
            status_message = 'Limite de llamadas a la API alcanzado'
            
        phone_obj = Phone.objects.create(
            phone = user_number,
            is_valid = is_valid,
            message = status_message
        )
        
        return Response({
            phone_obj.message #Esto deberia mostrar un texto diciendo si la url es valida o no
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
                'message' : sms_obj.message #Esto deberia mostrar un texto diciendo si la url es valida o no
            })
            
        validation_message, valido = verify_sms(request, message_sms)
        
        # Inicializar is_valid y status_message con valores predeterminados
        is_valid = valido  # Asume que es inseguro por defecto
        status_message = validation_message

        
        sms_obj = Sms.objects.create(
            message_sms = message_sms,
            is_valid = is_valid,
            message = status_message
        )
        
        return Response({
            sms_obj.message #Esto deberia mostrar un texto diciendo si la url es valida o no
        })