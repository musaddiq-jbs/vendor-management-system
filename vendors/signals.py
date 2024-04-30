from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    vendor = instance.vendor
    
    # Recalculate on-time delivery rate
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_delivery_count = completed_pos.filter(delivery_date__lte=F('delivery_date')).count()
    vendor.on_time_delivery_rate = on_time_delivery_count / completed_pos.count() if completed_pos else 0

    # Recalculate quality rating average
    quality_ratings = completed_pos.exclude(quality_rating=None).values_list('quality_rating', flat=True)
    vendor.quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if quality_ratings else 0

    # Recalculate average response time
    response_times = []
    for po in completed_pos:
        if po.acknowledgment_date:
            response_time = (po.acknowledgment_date - po.issue_date).total_seconds()
            response_times.append(response_time)
    vendor.average_response_time = sum(response_times) / len(response_times) if response_times else 0

    # Recalculate fulfillment rate
    fulfilled_pos = completed_pos.filter(fulfilled_without_issues=True).count()
    vendor.fulfillment_rate = fulfilled_pos / vendor.purchaseorder_set.count() if vendor.purchaseorder_set.exists() else 0

    vendor.save()