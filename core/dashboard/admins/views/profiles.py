from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from ...permissions import HasAdminAccessPermission
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from accounts.models import Profile
from django.contrib import messages
from ..forms import AdminPasswordChangeForm, AdminProfileEditForm, AdminProfileImageEditForm

class AdminSecurityEdit(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = "dashboard/admin/profiles/security-edit.html"
    success_message = "رمزعبور شما با موفقیت تغییر کرد ."
    success_url = reverse_lazy("dashboard:dash_admin:security-edit")
    form_class = AdminPasswordChangeForm

class AdminProfileEdit(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    form_class = AdminProfileEditForm
    template_name = "dashboard/admin/profiles/profile-edit.html"
    success_message = "اطلاعات هویتی شما با موفقیت تغییر کرد ."
    success_url = reverse_lazy("dashboard:dash_admin:profile-edit")

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    

class AdminProfileImageEdit(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    model = Profile
    fields = ["image"]
    template_name = "dashboard/admin/profiles/profile-edit.html"
    success_message = "اطلاعات هویتی شما با موفقیت تغییر کرد ."
    success_url = reverse_lazy("dashboard:dash_admin:profile-edit")
    http_method_names = ["post"]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
    def form_invalid(self, form):
        messages.error(self.request,"ارسال تصویر با مشکل مواجه شد . لطفا محددا بررسی و تلاش نمایید . ")
        return redirect(self.success_url)