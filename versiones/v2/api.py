from pagos.models import Services, Payment_user, Expired_payments
from rest_framework import viewsets
from .serializers import ServiceSerializer, PaymentUserSerializer, ExpiredPaymentsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, filters , permissions , status
from .pagination import StandardResultsSetPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class ServicesViewSet(viewsets.ModelViewSet):
    queryset = Services.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['id_services','name']
    search_fields = ['name']
    throttle_scope = 'pagos'
    
    def get_serializer_class(self):
        return ServiceSerializer
    
    
    def get_permissions(self):
        permission_classes = []

        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]

        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy' or self.action == 'retrieve' or self.action == 'create':
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]
    
    def retrieve(self, request, pk=None):
        service = get_object_or_404(self.queryset, pk=pk)
        serializer = ServiceSerializer(service)

        return Response(serializer.data)

    def create(self, request):

        if isinstance(request.data, list):
            serializer = ServiceSerializer(data=request.data, many = True)
        else:
            serializer = ServiceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        service = get_object_or_404(self.queryset, pk=pk)
        serializer = ServiceSerializer(service, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        service = get_object_or_404(self.queryset, pk=pk)
        serializer = ServiceSerializer(service, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        service = get_object_or_404(self.queryset, pk=pk)
        service.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class PaymentUserViewSet(viewsets.ModelViewSet):
    queryset = Payment_user.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['id_payment','user_id','service_id']
    search_fields = ['paymentDate', 'expirationDate']
    throttle_scope = 'pagos'

    def get_serializer_class(self):
        return PaymentUserSerializer


    def get_permissions(self):
        permission_classes = []

        if self.action == 'create' or self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]

        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy' or self.action == 'retrieve':
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]
    
    def retrieve(self, request, pk=None):
        payment = get_object_or_404(self.queryset, pk=pk)
        serializer = PaymentUserSerializer(payment)

        return Response(serializer.data)

    def create(self, request):

        if isinstance(request.data, list):
            serializer = PaymentUserSerializer(data=request.data, many = True)
        else:
            serializer = PaymentUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            if isinstance(request.data, list):
                lista = []
                for i in range(len(request.data)):
                    if request.data[i]["expirationDate"] < serializer.data[i]["paymentDate"]:
                        lista.append({
                            "payment_user_id": serializer.data[i]["id_expired"],
                            "penalty_fee_amount": 15.00
                            })
                expired_serial=ExpiredPaymentsSerializer(data=lista, many=True)

                if expired_serial.is_valid():
                    ExpiredPaymentsViewSet.create(ExpiredPaymentsViewSet,request=expired_serial)
            else:
                if request.data["expirationDate"] < serializer.data["paymentDate"]:
                    expired_serial=ExpiredPaymentsSerializer(data={
                        "payment_user_id": serializer.data["id_expired"],
                        "penalty_fee_amount": 15.00
                        })
                        
                    if expired_serial.is_valid():
                        ExpiredPaymentsViewSet.create(ExpiredPaymentsViewSet,request=expired_serial)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        payment = get_object_or_404(self.queryset, pk=pk)
        serializer = PaymentUserSerializer(payment, data=request.data)

        if serializer.is_valid():
            serializer.save()

            if request.data["expirationDate"] < serializer.data["paymentDate"]:
                expired_serial=ExpiredPaymentsSerializer(data={
                    "payment_user_id": serializer.data["id_expired"],
                    "penalty_fee_amount": 15.00
                    })
                    
                if expired_serial.is_valid():
                    ExpiredPaymentsViewSet.create(ExpiredPaymentsViewSet,request=expired_serial)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        payment = get_object_or_404(self.queryset, pk=pk)
        serializer = PaymentUserSerializer(payment, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            if request.data["expirationDate"] < serializer.data["paymentDate"]:
                expired_serial=ExpiredPaymentsSerializer(data={
                    "payment_user_id": serializer.data["id_expired"],
                    "penalty_fee_amount": 15.00
                    })
                    
                if expired_serial.is_valid():
                    ExpiredPaymentsViewSet.create(ExpiredPaymentsViewSet,request=expired_serial)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        payment = get_object_or_404(self.queryset, pk=pk)
        payment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    


class ExpiredPaymentsViewSet(viewsets.ModelViewSet):

    queryset = Expired_payments.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['id_expired','payment_user_id','penalty_fee_amount']
    search_fields = ['payment_user_id','penalty_fee_amount']
    throttle_scope = 'pagos'
    
    def get_serializer_class(self):
        return ExpiredPaymentsSerializer
    
    
    def get_permissions(self):
        permission_classes = []

        if self.action == 'create' or self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]

        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy' or self.action == 'retrieve':
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]
    
    def retrieve(self, request, pk=None):
        expired = get_object_or_404(self.queryset, pk=pk)
        serializer = ExpiredPaymentsSerializer(expired)

        return Response(serializer.data)

    def create(self, request):

        if isinstance(request.data, list):
            serializer = ExpiredPaymentsSerializer(data=request.data, many = True)
        else:
            serializer = ExpiredPaymentsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        expired = get_object_or_404(self.queryset, pk=pk)
        serializer = ExpiredPaymentsSerializer(expired, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        expired = get_object_or_404(self.queryset, pk=pk)
        serializer = ExpiredPaymentsSerializer(expired, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        expired = get_object_or_404(self.queryset, pk=pk)
        expired.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)