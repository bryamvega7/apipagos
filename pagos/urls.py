from versiones.v1 import api as api_v1
from versiones.v2 import api as api_v2
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'pagos', api_v1.PagoViewSet, 'pagos')
router.register(r'services', api_v2.ServicesViewSet, 'services')

urlpatterns = router.urls