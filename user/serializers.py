from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number', 'address', 'commune', 'role']
    
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_email(self, value):
        # Check if email is unique
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

    def create(self, validated_data):
        # Create user and set password
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        # Send email verification link
        self.send_verification_email(user)

        return user
    
    def send_verification_email(self, user):
        """
        Sends an email with a verification link to the user.
        """
        verification_token = get_random_string(20)  # Create a unique token
        verification_link = f"{settings.FRONTEND_URL}/verify-email/?token={verification_token}"

        send_mail(
            subject="Verify Your Email Address",
            message=f"Click on the link below to verify your email address: \n{verification_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
