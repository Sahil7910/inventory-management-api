from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class JWTAuthenticationTests(APITestCase):

    def setUp(self):
        # Create a test user for login and token retrieval
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_obtain_token_pair(self):
        """Test obtaining JWT token pair (access and refresh tokens)"""
        # Login with valid credentials and get the token
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(reverse('token_obtain_pair'), data)

        # Check the response status and whether tokens are present
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_obtain_invalid_credentials(self):
        """Test JWT token retrieval with invalid credentials"""
        # Attempt to login with wrong credentials
        data = {'username': 'wronguser', 'password': 'wrongpassword'}
        response = self.client.post(reverse('token_obtain_pair'), data)

        # Response should be 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        """Test refreshing the JWT access token using a valid refresh token"""
        # First, obtain the token pair
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(reverse('token_obtain_pair'), data)
        refresh_token = response.data['refresh']

        # Now use the refresh token to obtain a new access token
        refresh_data = {'refresh': refresh_token}
        refresh_response = self.client.post(reverse('token_refresh'), refresh_data)

        # Check if new access token is issued
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

    def test_refresh_token_invalid(self):
        """Test refreshing the JWT token with an invalid/expired refresh token"""
        # Provide an invalid or expired refresh token
        invalid_refresh_token = 'invalidtoken'
        refresh_data = {'refresh': invalid_refresh_token}
        refresh_response = self.client.post(reverse('token_refresh'), refresh_data)

        # Should return 401 Unauthorized
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_protected_route_with_valid_token(self):
        """Test accessing a protected route with a valid JWT access token"""
        # First, obtain a valid token pair
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(reverse('token_obtain_pair'), data)
        access_token = response.data['access']

        # Set the authorization header with the access token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        # Attempt to access a protected route (replace with actual protected route)
        protected_url = reverse('item-list')  # Example of a protected endpoint
        response = self.client.get(protected_url)

        # Expecting a 200 OK response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_protected_route_with_invalid_token(self):
        """Test accessing a protected route with an invalid JWT token"""
        # Set an invalid token in the authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')

        # Attempt to access a protected route (replace with actual protected route)
        protected_url = reverse('item-list')  # Example of a protected endpoint
        response = self.client.get(protected_url)

        # Expecting a 401 Unauthorized response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
