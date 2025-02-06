import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import scanned_codes
from django.views.generic import TemplateView

def scan_qr(request):
    return render(request, 'qrscanner/index.html')

@csrf_exempt
def process_qr_code(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            qr_code_value = body.get('qr_code')
            if not qr_code_value:
                return JsonResponse({"success": False, "message": "No QR code provided"}, status=400)
            try:
                obj = scanned_codes.objects.get(qr_code=qr_code_value)
                obj.scanned_count += 1
                obj.save()
                return JsonResponse({
                    "success": True,
                    "message": "QR code found in DB",
                    "name": obj.name,
                    "scanned_count": obj.scanned_count
                })
            except scanned_codes.DoesNotExist:
                return JsonResponse({"success": False, "message": "QR code not recognized in the database"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON"}, status=400)

class InventoryView(TemplateView):


    template_name = "qrscanner/items.html"