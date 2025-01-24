from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login as auth_login, logout

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication

@api_view(['POST'])
def login(request):
    
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        auth_login(request, user)  # Inicia sesión y crea una cookie de sesión
        return Response({"message": f"Logged in as {user.username}"})
    else:
        return Response({"error": "Invalid credentials"}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"message": "Logged out successfully"})



@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])  # Hashear la contraseña
        user.save()
        
        # Autenticar al usuario después de registrarlo
        authenticated_user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if authenticated_user:
            auth_login(request._request, authenticated_user)  # Usar el objeto HttpRequest
            
        return Response({'message': 'User registered and logged in successfully.'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    
    print(request.user)
    
    return Response("You are login with {}".format(request.user.username), status=status.HTTP_200_OK)