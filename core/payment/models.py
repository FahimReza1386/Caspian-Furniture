from django.db import models
from django.db.models import JSONField
# Create your models here.


class PaymentStatusType(models.IntegerChoices):
    pending = 1, "در انتظار"
    success = 2, "پرداخت موفق"
    failed = 3, "پرداخت ناموفق"


class PaymentModel(models.Model):
    authority_id = models.CharField(max_length=300)
    ref_id = models.BigIntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, default=0, decimal_places=0)
    response_json = JSONField(default=dict)
    response_code = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(choices=PaymentStatusType.choices, default=PaymentStatusType.pending.value)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)