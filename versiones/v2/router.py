from . import api
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'service', api.PagoViewSet, 'servicesView')

api_urlpatterns = router.urls