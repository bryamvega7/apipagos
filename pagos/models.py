from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
# Create your models here.

class Pagos(models.Model):
    class Servicios(models.TextChoices):
        NETFLIX = 'NF', _('Netflix')
        AMAZON = 'AP', _('Amazon Video')
        START = 'ST', _('Start+')
        PARAMOUNT = 'PM', _('Paramount+')

    servicio = models.CharField(
        max_length=2,
        choices=Servicios.choices,
        default=Servicios.NETFLIX,
    )
    fecha_pago = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete =models.CASCADE, related_name='users')
    monto = models.FloatField(default=0.0)
    
class Services(models.Model):
    id_services = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    logo = models.URLField()

class Payment_user(models.Model):
    id_payment = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Services, on_delete=models.CASCADE)
    amount =  models.FloatField(default=0.0)
    paymentDate = models.DateField(auto_now_add=True)
    expirationDate = models.DateField()
    
class Expired_payments(models.Model):
    id_expired = models.AutoField(primary_key=True)
    payment_user_id = models.ForeignKey(Payment_user, on_delete=models.CASCADE)
    penalty_fee_amount = models.FloatField(default=0.0)
