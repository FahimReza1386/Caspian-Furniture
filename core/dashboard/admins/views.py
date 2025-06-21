from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission

class AdminDashBoardHomeView(HasAdminAccessPermission, LoginRequiredMixin, TemplateView):
    template_name = "dashboard/admin/home.html"