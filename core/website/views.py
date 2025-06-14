from django.shortcuts import render
from django.views.generic import TemplateView
from cart.cart import CartSession
# Create your views here.

class IndexView(TemplateView):
    template_name="website/Home.html"

class AboutPageView(TemplateView):
    template_name="website/About.html"

class ContactPageView(TemplateView):
    template_name="website/Contact.html"