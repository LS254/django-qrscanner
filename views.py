import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ScannedCodes

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
                obj = ScannedCodes.objects.get(qr_code=qr_code_value)
                obj.scanned_count += 1
                obj.save()
                return JsonResponse({
                    "success": True,
                    "message": "QR code found in DB",
                    "name": obj.name,
                    "scanned_count": obj.scanned_count
                })
            except ScannedCodes.DoesNotExist:
                return JsonResponse({"success": False, "message": "QR code not recognized in the database"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON"}, status=400)

def item_list(request):
    items = ScannedCodes.objects.all() 

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add":
            qr_code = request.POST.get("qr_code")  
            name = request.POST.get("name")  
            if qr_code and name:
                ScannedCodes.objects.create(qr_code=qr_code, name=name, scanned_count=0)

        elif action == "remove":
            qr_code = request.POST.get("qr_code")
            ScannedCodes.objects.filter(qr_code=qr_code).delete()

        return redirect("item_list")
    
    return render(request, "qrscanner/items.html", {"items": items})