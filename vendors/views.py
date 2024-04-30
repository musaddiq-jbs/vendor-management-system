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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class VendorViewSet(viewsets.ModelViewSet):
    """
    Vendor API endpoints.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='List all vendors',
        operation_description='Returns a paginated list of all vendors.',
        responses={200: VendorSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Retrieve a vendor',
        operation_description='Returns the details of a specific vendor.',
        responses={200: VendorSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Create a vendor',
        operation_description='Creates a new vendor.',
        request_body=VendorSerializer,
        responses={201: VendorSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Update a vendor',
        operation_description='Updates the details of a specific vendor.',
        request_body=VendorSerializer,
        responses={200: VendorSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Partially update a vendor',
        operation_description='Partially updates the details of a specific vendor.',
        request_body=VendorSerializer,
        responses={200: VendorSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Delete a vendor',
        operation_description='Deletes a specific vendor.',
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    """
    Purchase Order API endpoints.
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='List all purchase orders',
        operation_description='Returns a paginated list of all purchase orders.',
        responses={200: PurchaseOrderSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Retrieve a purchase order',
        operation_description='Returns the details of a specific purchase order.',
        responses={200: PurchaseOrderSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Create a purchase order',
        operation_description='Creates a new purchase order.',
        request_body=PurchaseOrderSerializer,
        responses={201: PurchaseOrderSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Update a purchase order',
        operation_description='Updates the details of a specific purchase order.',
        request_body=PurchaseOrderSerializer,
        responses={200: PurchaseOrderSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Partially update a purchase order',
        operation_description='Partially updates the details of a specific purchase order.',
        request_body=PurchaseOrderSerializer,
        responses={200: PurchaseOrderSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Delete a purchase order',
        operation_description='Deletes a specific purchase order.',
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@swagger_auto_schema(
    method='get',
    operation_summary='Retrieve vendor performance metrics',
    operation_description='Returns the performance metrics for a specific vendor.',
    manual_parameters=[
        openapi.Parameter('vendor_id', openapi.IN_PATH, 'The ID of the vendor', type=openapi.TYPE_INTEGER),
    ],
    responses={200: openapi.Response('Vendor performance metrics', schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'on_time_delivery_rate': openapi.Schema(type=openapi.TYPE_NUMBER),
            'quality_rating_avg': openapi.Schema(type=openapi.TYPE_NUMBER),
            'average_response_time': openapi.Schema(type=openapi.TYPE_NUMBER),
            'fulfillment_rate': openapi.Schema(type=openapi.TYPE_NUMBER),
        }
    ))}
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def vendor_performance(request, vendor_id):
    """
    Retrieve vendor performance metrics.

    Returns the performance metrics for a specific vendor, including:
    - On-time delivery rate
    - Quality rating average
    - Average response time
    - Fulfillment rate

    Parameters:
    - vendor_id (integer): The ID of the vendor.

    Returns:
    - 200 OK: A JSON object containing the vendor's performance metrics.
    - 404 Not Found: If the vendor with the specified ID does not exist.

    Authentication:
    - JWT authentication required. Include the access token in the Authorization header as "Bearer {access_token}".

    Permissions:
    - User must be authenticated to access this endpoint.
    """
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

@swagger_auto_schema(
    method='post',
    operation_summary='Acknowledge a purchase order',
    operation_description='Updates the acknowledgment date of a specific purchase order.',
    manual_parameters=[
        openapi.Parameter('po_id', openapi.IN_PATH, 'The ID of the purchase order to acknowledge', type=openapi.TYPE_INTEGER),
    ],
    responses={
        200: openapi.Response('Purchase order acknowledged successfully'),
        404: openapi.Response('Purchase order not found'),
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def acknowledge_purchase_order(request, po_id):
    """
    Acknowledge a purchase order.

    Updates the acknowledgment date of a specific purchase order.

    Parameters:
    - po_id (integer): The ID of the purchase order to acknowledge.

    Returns:
    - 200 OK: If the purchase order is successfully acknowledged.
    - 404 Not Found: If the purchase order with the specified ID does not exist.

    Authentication:
    - JWT authentication required. Include the access token in the Authorization header as "Bearer {access_token}".

    Permissions:
    - User must be authenticated to access this endpoint.
    """
    try:
        po = PurchaseOrder.objects.get(id=po_id)
        po.acknowledgment_date = timezone.now()
        po.save()
        return Response({'message': 'PO acknowledged successfully.'})
    except PurchaseOrder.DoesNotExist:
        return Response({'message': 'PO not found.'}, status=404)