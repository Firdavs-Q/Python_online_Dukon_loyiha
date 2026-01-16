from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class HOMEPageView(TemplateView):
    template_name='homeP.html'
    
class SavatView(TemplateView):
    template_name='savatP.html'