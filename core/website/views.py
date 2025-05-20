from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class IndexView(TemplateView):
    template_name="website/Home.html"


class AboutPageView(TemplateView):
    template_name="website/About.html"