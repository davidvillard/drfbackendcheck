from rest_framework import routers
from .views import EmailViewSet, UrlViewSet, PhoneViewSet, SmsViewSet

router = routers.DefaultRouter()

router.register(r'api/verifier/url', UrlViewSet, 'verifierUrl')
router.register(r'api/verifier/email', EmailViewSet, 'verifierEmail')
router.register(r'api/verifier/phone', PhoneViewSet, 'verifierPhone')
router.register(r'api/verifier/sms', SmsViewSet, 'verifierSms')

urlpatterns = router.urls
