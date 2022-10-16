import uuid
import os
from django.db import IntegrityError, models


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

from app.storage_backends import PublicMediaStorage, PrivateMediaStorage



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, username="", **extra_fields):
        """Creates and save a new user"""
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Creates and saves a superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_photo_url = models.FileField(null=True,storage=PublicMediaStorage())
    cover_photo_url = models.FileField(null=True,storage=PublicMediaStorage())
    phone_number = models.CharField(max_length=255, blank=True)
    organized_events_list = models.ManyToManyField('Event', blank=True)
    fav_vendors = models.ManyToManyField('Vendor', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class VendorCategory(models.Model):
    """Category for vendors"""
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    logo = models.FileField(storage=PublicMediaStorage())
    picture = models.FileField(null=True,storage=PublicMediaStorage())

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Review model for vendors"""
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    vendor = models.ForeignKey(
        'Vendor', on_delete=models.CASCADE, related_name='reviews')
    review_text = models.CharField(max_length=255)
    rating = rating = models.DecimalField(
        max_digits=3, decimal_places=2, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EventType(models.Model):
    """Event type model"""
    type_name = models.CharField(max_length=255)
    type_of_vendors_needed = models.ManyToManyField('Vendor')
    logo = models.FileField(null=True,storage=PublicMediaStorage())
    picture = models.FileField(null=True,storage=PublicMediaStorage())

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type_name


class Offer(models.Model):
    """Offer model for vendors"""
    vendor = models.ForeignKey(
        'Vendor', on_delete=models.CASCADE, related_name='offers')
    heading = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class VendorPhoto(models.Model):
    image = models.FileField(storage=PublicMediaStorage())
    vendor = models.ForeignKey(
        'Vendor', on_delete=models.CASCADE, related_name='photos')


class EventPhoto(models.Model):
    image = models.FileField(storage=PublicMediaStorage())
    vendor = models.ForeignKey(
        'Event', on_delete=models.CASCADE, related_name='photos')


class Vendor(models.Model):
    """Vendor model"""

    title = models.CharField(max_length=255, blank=False)
    followers = models.IntegerField(default=0)
    description = models.CharField(max_length=2000)
    category = models.ForeignKey(
        'VendorCategory', on_delete=models.CASCADE, related_name='vendors')
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)
    location_str = models.CharField(max_length=255)
    cover_photo = models.FileField(null=False,storage=PublicMediaStorage())
    poster_photo=models.FileField(null=False,storage=PublicMediaStorage())
    rating=models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    number_of_rating=models.IntegerField(default=0)
    fb_profile_url=models.CharField(max_length=255, blank=True)
    insta_profile_url=models.CharField(max_length=255, blank=True)
    contact_number=models.CharField(max_length=255, blank=False)
    website_url=models.CharField(max_length=255, blank=True)
    pinterest_url=models.CharField(max_length=255, blank=True)
    total_liked=models.IntegerField(default=0)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Event(models.Model):
    """Event model"""

    title=models.CharField(max_length=255, blank=True)
    description=models.CharField(max_length=2000)
    event_type=models.ForeignKey(
        'EventType', on_delete=models.CASCADE, related_name='events')
    latitude=models.FloatField(blank=True)
    longitude=models.FloatField(blank=True)
    venue_str=models.CharField(max_length=255, blank=True)
    location_str=models.CharField(max_length=255, blank=False)
    date_of_event=models.DateTimeField()
    cover_photo=models.FileField(null=False,storage=PublicMediaStorage())
    vendor_list=models.ManyToManyField('Vendor')
    total_liked=models.IntegerField(default=0)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
