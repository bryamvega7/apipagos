from rest_framework import serializers
from pagos.models import Pagos

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagos
        fields = '__all__'