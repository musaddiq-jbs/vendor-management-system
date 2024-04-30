from rest_framework import serializers
from .models import Vendor, PurchaseOrder

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        extra_kwargs = {
            'address': {'required': False},
            'contact_details': {'required': False},
            'on_time_delivery_rate': {'required': False},
            'quality_rating_avg': {'required': False},
            'average_response_time': {'required': False},
            'fulfillment_rate': {'required': False},
        }

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.contact_details = validated_data.get('contact_details', instance.contact_details)
        instance.address = validated_data.get('address', instance.address)
        instance.vendor_code = validated_data.get('vendor_code', instance.vendor_code)
        instance.on_time_delivery_rate = validated_data.get('on_time_delivery_rate', instance.on_time_delivery_rate)
        instance.quality_rating_avg = validated_data.get('quality_rating_avg', instance.quality_rating_avg)
        instance.average_response_time = validated_data.get('average_response_time', instance.average_response_time)
        instance.fulfillment_rate = validated_data.get('fulfillment_rate', instance.fulfillment_rate)
        instance.save()
        return instance

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        extra_kwargs = {
            'quality_rating': {'required': False},
            'acknowledgment_date': {'required': False},
            'fulfilled_without_issues': {'required': False},
            'po_number': {'required': False},
            'delivery_date': {'required': False},
            'items': {'required': False},
            'quantity': {'required': False},
            'vendor': {'required': False},
        }

    def update(self, instance, validated_data):
        instance.po_number = validated_data.get('po_number', instance.po_number)
        instance.vendor = validated_data.get('vendor', instance.vendor)
        instance.delivery_date = validated_data.get('delivery_date', instance.delivery_date)
        instance.items = validated_data.get('items', instance.items)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.status = validated_data.get('status', instance.status)
        instance.quality_rating = validated_data.get('quality_rating', instance.quality_rating)
        instance.acknowledgment_date = validated_data.get('acknowledgment_date', instance.acknowledgment_date)
        instance.fulfilled_without_issues = validated_data.get('fulfilled_without_issues', instance.fulfilled_without_issues)
        instance.save()
        return instance