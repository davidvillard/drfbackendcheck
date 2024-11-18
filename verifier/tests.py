from django.test import TestCase
from .validators import verify_sms  # Asegúrate de importar la función correctamente

# Create your tests here.
class SmsValidatorTestCase(TestCase):
    def test_verify_sms(self):
        mensaje_1 = "Felicidades ganaste un premio: www.fake-url.com"
        mensaje_2 = "No hay ninguna URL en este mensaje"
        mensaje_3 = "¡Oferta especial! Visita: www.descuentos.com"

        print(verify_sms(mensaje_1))  # Esperado: "www.fake-url.com"
        print(verify_sms(mensaje_2))  # Esperado: "No se encontró una URL en el mensaje"
        print(verify_sms(mensaje_3))  # Esperado: "www.descuentos.com"

            