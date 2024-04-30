from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Vendor, PurchaseOrder

class VendorTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        self.vendor_data = {
            'name': 'Test Vendor',
            'contact_details': 'test@vendor.com',
            'address': '123 Test Street',
            'vendor_code': 'TEST001'
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

    def test_create_vendor(self):
        url = reverse('vendor-list')
        response = self.client.post(url, self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)

    def test_get_vendor_list(self):
        url = reverse('vendor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_vendor_detail(self):
        url = reverse('vendor-detail', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.vendor_data['name'])

    def test_update_vendor(self):
        url = reverse('vendor-detail', args=[self.vendor.id])
        updated_data = {'name': 'Updated Vendor'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, updated_data['name'])

    def test_delete_vendor(self):
        url = reverse('vendor-detail', args=[self.vendor.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)

class PurchaseOrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        self.vendor = Vendor.objects.create(name='Test Vendor', vendor_code='TEST001')
        self.po_data = {
            'po_number': 'PO001',
            'vendor': self.vendor.id,
            'delivery_date': '2023-06-30',
            'items': [{'name': 'Item 1', 'quantity': 10}],
            'quantity': 10,
            'status': 'pending'
        }
        self.po = PurchaseOrder.objects.create(**self.po_data)

    def test_create_purchase_order(self):
        url = reverse('purchaseorder-list')
        response = self.client.post(url, self.po_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)

    def test_get_purchase_order_list(self):
        url = reverse('purchaseorder-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_purchase_order_detail(self):
        url = reverse('purchaseorder-detail', args=[self.po.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], self.po_data['po_number'])

    def test_update_purchase_order(self):
        url = reverse('purchaseorder-detail', args=[self.po.id])
        updated_data = {'status': 'completed'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.po.refresh_from_db()
        self.assertEqual(self.po.status, updated_data['status'])

    def test_delete_purchase_order(self):
        url = reverse('purchaseorder-detail', args=[self.po.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)

    def test_acknowledge_purchase_order(self):
        url = reverse('acknowledge-purchase-order', args=[self.po.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.po.refresh_from_db()
        self.assertIsNotNone(self.po.acknowledgment_date)

class VendorPerformanceTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        self.vendor = Vendor.objects.create(name='Test Vendor', vendor_code='TEST001')
        self.po1 = PurchaseOrder.objects.create(
            po_number='PO001', vendor=self.vendor, delivery_date='2023-06-30',
            items=[{'name': 'Item 1', 'quantity': 10}], quantity=10, status='completed',
            quality_rating=4.5, fulfilled_without_issues=True
        )
        self.po2 = PurchaseOrder.objects.create(
            po_number='PO002', vendor=self.vendor, delivery_date='2023-07-15',
            items=[{'name': 'Item 2', 'quantity': 5}], quantity=5, status='pending'
        )

    def test_get_vendor_performance(self):
        url = reverse('vendor-performance', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['on_time_delivery_rate'], 1.0)
        self.assertEqual(response.data['quality_rating_avg'], 4.5)
        self.assertEqual(response.data['fulfillment_rate'], 0.5)