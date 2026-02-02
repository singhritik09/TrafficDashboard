from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
# Create your views here.

class HomeView(View):
    def get(self, request):
        template_name = 'home.html'
        # return HttpResponse("Welcome to the Home Page!")    
        return render(request, template_name)

class StatusView(View):
    def get(self, request):
        return HttpResponse("Status: OK", status=200)   