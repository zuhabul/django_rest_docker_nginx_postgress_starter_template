from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from core.models import VendorCategory, Review, Offer, Vendor , VendorPhoto


class VendorCategorySerializer(serializers.ModelSerializer):
    """Serializer for Vendor Category objects"""

    class Meta:
        model = VendorCategory
        fields = (
            'id',
            'name',
            'description',
            'logo',
            'picture'
        )
        read_only_fields = ['id', 'name' ]


class OfferSerializer(serializers.ModelSerializer):
    """Serializer for offer objects"""

    class Meta:
        model = Offer
        depth = 0
        fields = (
            'id',
            'vendor',
            'heading',
            'description',
        )
        read_only_fields = ['id']

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for review objects"""

    class Meta:
        model = Review
        fields = (
            'id',
            'user',
            'vendor',
            'review_text',
            'rating',
            'created_at',
            'updated_at'
        )
        read_only = True


class VendorPhotoSerializer(serializers.ModelSerializer):
    """Serializer for uploading cover photo to vendor"""

    class Meta:
        model = VendorPhoto
        fields = ('id', 'image')
        read_only_fields = ['id', ]


class VendorSerializer(serializers.ModelSerializer):
    """Serializer for vendor objects"""
    reviews = ReviewSerializer(many=True)
    photos = VendorPhotoSerializer(many=True)
    offers = OfferSerializer(many=True)
    class Meta:
        model = Vendor
        depth = 0
        # fields = '__all__'
        fields = (
            'id',
            'title',
            'description',
            'category',
            'latitude',
            'longitude',
            'location_str',
            'rating',
            'cover_photo',
            'poster_photo',
            'number_of_rating',
            'fb_profile_url',
            'insta_profile_url',
            'contact_number',
            'website_url',
            'pinterest_url',
            'total_liked',
            'reviews',
            'photos',
            'offers',
        )

        read_only_fields = ['id', ]




#Uploading pictures viewsets
class PosterPhotoImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading poster photo to vendor"""

    class Meta:
        model = Vendor
        fields = ('id', 'poster_photo')
        read_only_fields = ['id', ]


class GalleryPhotoImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading gallery photo to vendor"""

    class Meta:
        model = Vendor
        fields = ('id', 'gallery_photo')
        read_only_fields = ['id', ]


class VendorCategoryLogoSerializer(serializers.ModelSerializer):
    """Serializer for uploading vendor category logo to vendor category"""

    class Meta:
        model = VendorCategory
        fields = ('id', 'logo')
        read_only_fields = ['id', ]


class GalleryPhotoImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading vendor category image to vendor category"""

    class Meta:
        model = VendorCategory
        fields = ('id', 'picture')
        read_only_fields = ['id', ]
