from rest_framework import viewsets
from django.db.models import F
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def vendor_performance(request, vendor_id):
    vendor = Vendor.objects.get(id=vendor_id)
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')

    on_time_delivery_count = completed_pos.filter(delivery_date__lte=F('delivery_date')).count()
    on_time_delivery_rate = on_time_delivery_count / completed_pos.count() if completed_pos else 0

    quality_ratings = completed_pos.exclude(quality_rating=None).values_list('quality_rating', flat=True)
    quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if quality_ratings else 0

    response_times = []
    for po in completed_pos:
        if po.acknowledgment_date:
            response_time = (po.acknowledgment_date - po.issue_date).total_seconds()
            response_times.append(response_time)
    average_response_time = sum(response_times) / len(response_times) if response_times else 0

    fulfilled_pos = completed_pos.filter(fulfilled_without_issues=True).count()
    fulfillment_rate = fulfilled_pos / vendor.purchaseorder_set.count() if vendor.purchaseorder_set.exists() else 0

    data = {
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_avg': quality_rating_avg,
        'average_response_time': average_response_time,
        'fulfillment_rate': fulfillment_rate,
    }
    return Response(data)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def acknowledge_purchase_order(request, po_id):
    try:
        po = PurchaseOrder.objects.get(id=po_id)
        po.acknowledgment_date = timezone.now()
        po.save()
        return Response({'message': 'PO acknowledged successfully.'})
    except PurchaseOrder.DoesNotExist:
        return Response({'message': 'PO not found.'}, status=404)