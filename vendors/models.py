from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField(blank=True)
    address = models.TextField(blank=True)
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    quality_rating_avg = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    average_response_time = models.FloatField(default=0, validators=[MinValueValidator(0)])
    fulfillment_rate = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    fulfilled_without_issues = models.BooleanField(default=False)

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()