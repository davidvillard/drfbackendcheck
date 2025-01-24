from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import requests
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import permission_classes, authentication_classes

class EmailAPIView(APIView):
    @authentication_classes([SessionAuthentication])
    @permission_classes([IsAuthenticated])
    def post(self, request):
        try:
            print(f"Datos recibidos: {request.data.get('message')}")  # Corrección de comillas
            to_email = request.user.email
            subject = "Mensaje de prueba"
            message = request.data.get("message")
            send_mail(subject, message, None, [to_email])
            return Response({"message": "Email enviado con éxito"}, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)
