from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from security_data.models import *
from user.models import *

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    commune = serializers.PrimaryKeyRelatedField(queryset=Commune.objects.all(), required=True)  # Mandatory
    image = serializers.ImageField(required=False, allow_null=True)  # Add image field

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'commune', 'phone_number', 'address', 'image']  # Include image
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_email(self, value):
        # Check if email is unique
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

    def create(self, validated_data):
        # Create user and set password
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # Hash the password
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
