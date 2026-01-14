from django.contrib import admin
from django.urls import include, path
from home_sahifa.views import home # type: ignore # View import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'), 
    path('sahifa/', home, name='sahif'),
]