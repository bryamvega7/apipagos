from . import api as api_v2
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'service', api_v2.ServicesViewSet, 'service')
router.register(r'payment', api_v2.PaymentUserViewSet, 'payment')
router.register(r'expired', api_v2.ExpiredPaymentsViewSet, 'expired')

api_urlpatterns = router.urls