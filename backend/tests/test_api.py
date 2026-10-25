import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from inventory.models import Vehicle
@pytest.mark.django_db
def test_registration_and_login():
    client=APIClient()
    response=client.post('/api/auth/register',{'username':'buyer','email':'buyer@example.com','password':'StrongPass123'},format='json')
    assert response.status_code==201
    response=client.post('/api/auth/login',{'username':'buyer','password':'StrongPass123'},format='json')
    assert response.status_code==200 and 'access' in response.data
@pytest.mark.django_db
def test_vehicle_list_requires_authentication():
    assert APIClient().get('/api/vehicles/').status_code==401
@pytest.mark.django_db
def test_purchase_decreases_stock_and_prevents_overselling():
    user=User.objects.create_user(username='buyer',password='StrongPass123')
    vehicle=Vehicle.objects.create(make='Toyota',model='Corolla',category='sedan',price='18000',quantity=1)
    client=APIClient(); client.force_authenticate(user=user)
    response=client.post(f'/api/vehicles/{vehicle.id}/purchase/',{'quantity':1},format='json')
    assert response.status_code==200
    vehicle.refresh_from_db(); assert vehicle.quantity==0
    assert client.post(f'/api/vehicles/{vehicle.id}/purchase/',{'quantity':1},format='json').status_code==400
@pytest.mark.django_db
def test_only_admin_can_delete_vehicle():
    vehicle=Vehicle.objects.create(make='Honda',model='Civic',category='sedan',price='20000',quantity=2)
    user=User.objects.create_user(username='buyer',password='StrongPass123')
    client=APIClient(); client.force_authenticate(user=user)
    assert client.delete(f'/api/vehicles/{vehicle.id}/').status_code==403
