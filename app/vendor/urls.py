from django.urls import path , include
from rest_framework.routers import DefaultRouter
from vendor import views

router = DefaultRouter()
router.register('', views.VendorViewSet)


app_name = 'vendor'

urlpatterns = [
    path('', include(router.urls)),
]