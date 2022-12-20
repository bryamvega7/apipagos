from pagos.models import Services
from rest_framework import viewsets
from .serializers import ServiceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, filters 

class ServicesViewSet(viewsets.ModelViewSet):
    queryset = Services.objects.get_queryset()
    serializer_class = ServiceSerializer
    # filter_backends = [filters.SearchFilter]
    permission_classes = [IsAuthenticated]

    # search_fields = ['usuario__id', 'fecha_pago', 'servicio']
    # throttle_scope = 'services'