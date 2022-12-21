from . import api as api_v1
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'pago', api_v1.PagoViewSet, 'pagosView')

api_urlpatterns = router.urls