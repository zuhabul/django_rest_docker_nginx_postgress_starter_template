from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    """Serializers for the user objects"""

    class Meta:
        depth = 1
        model = get_user_model()
        fields = ('email','password','name','profile_photo_url','cover_photo_url','phone_number','organized_events_list','fav_vendors')
        extra_kwargs = {'password': {'min_length': 5, 'write_only': True,},
}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it and overwrite default one"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""

        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save(self._db)
        return user
# Unused and kept for ref


class LoginSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    # def validate(self, attrs):
    #     """Validate and authenticate the user"""
    #     email = attrs.get('email')
    #     password = attrs.get('password')

    #     user = authenticate(
    #         request=self.context.get('request'),
    #         username=email,
    #         password=password,
    #     )
    #     if not user:
    #         msg = ('Unable to authenticate with provided information')
    #         raise serializers.ValidationError(msg, code='authenticate')

    #     attrs['user'] = user
    #     return attrs


class SocialSerializer(serializers.Serializer):
    """Serializer which accepts an OAuth2 access token and provider."""
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(
        max_length=4096, required=True, trim_whitespace=True)


class SocialLoginResSerializer(serializers.Serializer):
    """Serializer which accepts an OAuth2 access token and provider"""
    access_token = serializers.CharField(max_length=255, required=True)
    expires_in = serializers.CharField(max_length=255, required=True)
    token_type = serializers.CharField(max_length=255, required=True)
    scope = serializers.CharField(max_length=255, required=True)
    refresh_token = serializers.CharField(max_length=255, required=True)


class LogoutSerializer(serializers.Serializer):
    """Serializer which accepts an OAuth2 access token and logs out user"""
    token = serializers.CharField(
        max_length=4096, required=True, trim_whitespace=True)


class UserImageUploadSerializer(serializers.Serializer):
    """Serializer for uploading profile image"""

    image_url = serializers.CharField(
        max_length=4096, required=True, trim_whitespace=True)
    image_type = serializers.CharField(
        max_length=4096, required=True, trim_whitespace=True)
