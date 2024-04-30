from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, PurchaseOrderViewSet, vendor_performance, acknowledge_purchase_order

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase_orders', PurchaseOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('vendors/<int:vendor_id>/performance/', vendor_performance, name='vendor-performance'),
    path('purchase_orders/<int:po_id>/acknowledge/', acknowledge_purchase_order, name='acknowledge-purchase-order'),
]