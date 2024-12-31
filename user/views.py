from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer


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


class RegisterUserView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated users
    
    def post(self, request):
        # Deserialize request data
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()  # Save the user and send email validation
            return Response({"message": "User created. Please check your email to verify your account."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckLoginView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this

    def get(self, request):
        return Response({"authenticated": True})