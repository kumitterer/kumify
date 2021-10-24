from django.views.generic import View
from django.http import JsonResponse

class StatusView(View):
    def get(self, request):
        return JsonResponse({"status": "OK", "messages": []})