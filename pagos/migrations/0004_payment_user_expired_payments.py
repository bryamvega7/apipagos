# Generated by Django 4.1.4 on 2022-12-20 20:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pagos', '0003_services'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment_user',
            fields=[
                ('id_payment', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.FloatField(default=0.0)),
                ('paymentDate', models.DateField(auto_now_add=True)),
                ('expirationDate', models.DateField()),
                ('service_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagos.services')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expired_payments',
            fields=[
                ('id_expired', models.AutoField(primary_key=True, serialize=False)),
                ('penalty_fee_amount', models.FloatField(default=0.0)),
                ('payment_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagos.payment_user')),
            ],
        ),
    ]
