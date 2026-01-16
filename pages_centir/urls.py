from django.urls import path
from .views import HOMEPageView , SavatView

urlpatterns = [
    path('',HOMEPageView.as_view(),name='home'),
    path('savat/',SavatView.as_view(),name='savat'),
]
