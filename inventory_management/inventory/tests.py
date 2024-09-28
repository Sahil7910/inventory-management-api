from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Item
from django.core.cache import cache


class InventoryCRUDTests(APITestCase):

    def setUp(self):
        # Create a test user and obtain a JWT token
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create an item in the database for testing
        self.item = Item.objects.create(name="Test Item", description="Test Description")

        # Obtain JWT token
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_item(self):
        """Test creating an inventory item"""
        data = {
            'name': 'New Item',
            'description': 'New Item Description'
        }
        response = self.client.post(reverse('item-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(Item.objects.get(id=2).name, 'New Item')

    def test_read_item(self):
        """Test retrieving an inventory item"""
        response = self.client.get(reverse('item-detail', args=[self.item.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Item')
        self.assertEqual(response.data['description'], 'Test Description')

    def test_update_item(self):
        """Test updating an inventory item"""
        data = {
            'name': 'Updated Item',
            'description': 'Updated Description'
        }
        response = self.client.put(reverse('item-update', args=[self.item.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Updated Item')
        self.assertEqual(self.item.description, 'Updated Description')

    def test_delete_item(self):
        """Test deleting an inventory item"""
        response = self.client.delete(reverse('item-delete', args=[self.item.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)

    def test_read_item_cache(self):
        """Test Redis caching for retrieving an inventory item"""
        # Clear the cache first
        cache.clear()

        # First request: should create the cache
        response = self.client.get(reverse('item-detail', args=[self.item.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Item')

        # Second request: should fetch from cache
        response_cached = self.client.get(reverse('item-detail', args=[self.item.id]))
        self.assertEqual(response_cached.status_code, status.HTTP_200_OK)
        self.assertEqual(response_cached.data['name'], 'Test Item')
