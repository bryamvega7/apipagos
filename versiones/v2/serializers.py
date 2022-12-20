from rest_framework import serializers
from pagos.models import Services

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'
        read_only_fields = '__all__',