from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated users
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(f"username {username} / password {password}")

        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('Invalid username or password!')

        # Create or retrieve a token
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'role': user.role,
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()  # Delete the token
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)