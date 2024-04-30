# Vendor Management System

The Vendor Management System is a Django-based web application that allows you to manage vendors, track purchase orders, and evaluate vendor performance metrics.

## Features

- Vendor Profile Management: Create, retrieve, update, and delete vendor profiles.
- Purchase Order Tracking: Create, retrieve, update, and delete purchase orders associated with vendors.
- Vendor Performance Evaluation: Calculate and retrieve performance metrics for each vendor, including on-time delivery rate, quality rating average, average response time, and fulfillment rate.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/vendor-management-system.git
   ```

2. Navigate to the project directory:

   ```bash
   cd vendor-management-system
   ```

3. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   - For Windows:

     ```bash
     venv\Scripts\activate
     ```

   - For macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

5. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

7. Create a superuser account:

   ```bash
   python manage.py createsuperuser
   ```

8. Start the development server:

   ```bash
   python manage.py runserver
   ```

9. Access the application in your web browser at `http://localhost:8000`.

## API Endpoints

The following API endpoints are available:

### Authentication

- Obtain an access token:
  - Endpoint: `POST /api/token/`
  - Request Body:

    ```json
    {
      "username": "your-username",
      "password": "your-password"
    }
    ```

### Vendor Endpoints

- Create a new vendor:
  - Endpoint: `POST /api/vendors/`
  - Request Body:

    ```json
    {
      "name": "New Vendor",
      "contact_details": "contact@newvendor.com",
      "address": "123 New Street",
      "vendor_code": "NEW001"
    }
    ```

- List all vendors:
  - Endpoint: `GET /api/vendors/`

- Retrieve a specific vendor's details:
  - Endpoint: `GET /api/vendors/{vendor_id}/`

- Update a vendor's details:
  - Endpoint: `PUT /api/vendors/{vendor_id}/`
  - Request Body:

    ```json
    {
      "name": "Updated Vendor",
      "contact_details": "updated@vendor.com"
    }
    ```

- Delete a vendor:
  - Endpoint: `DELETE /api/vendors/{vendor_id}/`

### Purchase Order Endpoints

- Create a purchase order:
  - Endpoint: `POST /api/purchase_orders/`
  - Request Body:

    ```json
    {
      "po_number": "PO001",
      "vendor": 1,
      "delivery_date": "2023-06-30",
      "items": [{"name": "Item 1", "quantity": 10}],
      "quantity": 10,
      "status": "pending"
    }
    ```

- List all purchase orders:
  - Endpoint: `GET /api/purchase_orders/`

- Retrieve details of a specific purchase order:
  - Endpoint: `GET /api/purchase_orders/{po_id}/`

- Update a purchase order:
  - Endpoint: `PUT /api/purchase_orders/{po_id}/`
  - Request Body:

    ```json
    {
      "status": "completed"
    }
    ```

- Delete a purchase order:
  - Endpoint: `DELETE /api/purchase_orders/{po_id}/`

- Acknowledge a purchase order:
  - Endpoint: `POST /api/purchase_orders/{po_id}/acknowledge/`

### Vendor Performance Endpoint

- Retrieve a vendor's performance metrics:
  - Endpoint: `GET /api/vendors/{vendor_id}/performance/`

## Authentication

The API endpoints are secured using token-based authentication (JWT). To access the protected endpoints, include the JWT token in the `Authorization` header of your requests as `Bearer your-access-token`.

## Testing

To run the test suite, execute the following command:

```bash
python manage.py test vendors
```

This will run all the tests defined in the `vendors/tests.py` file.
