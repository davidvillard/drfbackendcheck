from rest_framework import serializers
from .models import Url, Email, Phone, Sms

class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ('id', 'nombre_url', 'message', 'input_at')
        read_only_fields = ('input_at',)
        
class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ('id', 'email', 'message', 'input_at')
        read_only_fields = ('input_at',)
        
class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('id', 'phone', 'message', 'input_at')
        read_only_fields = ('input_at',)
        
class SmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sms
        fields = ('id', 'message_sms', 'message', 'input_at')
        read_only_fields = ('input_at',)