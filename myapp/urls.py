from django.urls import path 
from myapp.views import HomeView, StatusView
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),    
    path('', HomeView.as_view(), name='home'),
    path('status/', StatusView.as_view(), name='status'),
]