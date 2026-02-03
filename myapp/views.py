from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from django.http import JsonResponse
from myapp.security.traffic_buffer import get_traffic_buffer_snapshot, update_traffic_buffer, TRAFFIC_BUFFER

class HomeView(View):
    def get(self, request):
        template_name = 'home.html'
        context={}
        return render(request, template_name,context=context)

class StatusView(View):
    def get(self, request):
        # return HttpResponse("Status: OK", status=200)   
        return JsonResponse({"status": "ok", "traffic_stats": get_traffic_buffer_snapshot()})