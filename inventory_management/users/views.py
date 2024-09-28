from rest_framework import generics
from rest_framework_jwt.settings import api_settings
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



# For JWT Token Handling
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER





class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class ObtainJWTTokenView(generics.CreateAPIView):
#     def post(self, request, *args, **kwargs):
#         payload = jwt_payload_handler(request.user)
#         token = jwt_encode_handler(payload)
#         return Response({'token': token})

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response({'token': token})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)
