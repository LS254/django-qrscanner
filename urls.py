from django.urls import path
from . import views

urlpatterns = [
    path('', views.scan_qr, name='qrscanner'),
    path('scan/', views.process_qr_code, name='qrscanner-scan'),
    path('/inventory', views.item_list, name="item_list")
]
