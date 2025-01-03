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
from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated users

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('Invalid username or password!')

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'refresh': str(refresh),  # Refresh token
            'access': access_token,   # Access token
            'user_id': user.id,
            'username': user.username,
            'role': getattr(user, 'role', None),
        }, status=200)



class RegisterUserView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated users

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # Save the user
                user = serializer.save()

                # Optional: Send email verification (customize as per your app's requirement)
                if hasattr(serializer, 'send_email_verification'):
                    serializer.send_email_verification(user)

                return Response({
                    "message": "User created successfully. Please check your email to verify your account."
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)