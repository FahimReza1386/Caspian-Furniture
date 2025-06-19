from django import forms
from .models import UserAddressModel, CouponModel
from datetime import timezone
class CheckOutForm(forms.Form):
    address_id = forms.IntegerField(required=True)
    coupon = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(CheckOutForm, self).__init__(*args, **kwargs)


    def clean_address_id(self):
        address_id = self.cleaned_data.get("address_id")

        user = self.request.user

        try:
            address = UserAddressModel.objects.get(id=address_id, user=user)
        except UserAddressModel.DoesNotExist:
            raise forms.ValidationError("آدرسی ثبت نشده است .")
        
        return address

    def clean_coupon(self):
        code = self.cleaned_data.get("coupon")

        if code == "":
            return None
        
        user = self.request.user

        try :
            coupon = CouponModel.objects.get(code=code)
        except CouponModel.DoesNotExist:
            raise forms.ValidationError("کد تخفیف وارد شده وجود ندارد ..")

        if coupon:

            if coupon.used_by.count() >= coupon.max_limit_usage:
                raise forms.ValidationError("تعداد استفاده کنندگان از تخفیف به اتمام رسیده است ..")

            if coupon.expiration_date and coupon.expiration_date < timezone.now():
                raise forms.ValidationError("زمان استفاده از تخفیف به اتمام رسیده ..")
            
            if user in coupon.used_by.all():
                raise forms.ValidationError("این کد قبلا توسط شما استفاده شده است .")

        return coupon