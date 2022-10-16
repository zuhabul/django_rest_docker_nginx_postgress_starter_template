from rest_framework import generics, authentication, permissions, status, views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, LogoutSerializer, LoginSerializer, UserImageUploadSerializer
import os
from rest_framework.response import Response
from requests.exceptions import HTTPError

from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
from . import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
import json
from django.http.response import HttpResponse

from django.core.files.temp import NamedTemporaryFile
from django.core.files import File


import jwt
import requests
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from social_core.utils import handle_http_errors


class CreateUserView(generics.GenericAPIView):
    """Creates a new user to the system"""
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Create user and returns access_token"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="User could not be created")
        data = {
            "grant_type": "password",
            "username": serializer.validated_data['email'],
            "password": serializer.validated_data['password'],
            "client_id": os.environ.get('CLIENT_ID'),
            "client_secret": os.environ.get('CLIENT_SECRET')
        }
        if(settings.DEBUG):
            res = requests.post(
                'http://127.0.0.1:8000/api/user/oauth/token/',
                json=data)
            return Response(status=status.HTTP_200_OK, data=res.json())
        else:
            res = requests.post(
                'http://ec2-15-26-117-163.ap-south-1.compute.amazonaws.com/api/user/oauth/token/',
                json=data)

        return Response(status=status.HTTP_200_OK, data=res.json())


class LoginUserView(generics.GenericAPIView):
    """Logs in user to the system"""
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Logs in user to the system"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request=request,
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
        )
        if not user:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data="Incorrect email or password")
        user.is_active = True
        user.save()
        data = {
            "grant_type": "password",
            "username": serializer.validated_data['email'],
            "password": serializer.validated_data['password'],
            "client_id": os.environ.get('CLIENT_ID'),
            "client_secret": os.environ.get('CLIENT_SECRET')
        }
        if(settings.DEBUG):
            res = requests.post(
                'http://127.0.0.1:8000/api/user/oauth/token/',
                json=data, headers={'content-type': 'application/json'}, timeout=120)
            return Response(status=status.HTTP_200_OK, data=res.json())

        else:
            res = requests.post(
                'http://ec2-15-206-17-163.ap-south-1.compute.amazonaws.com/api/user/oauth/token/',
                json=data)
        return Response(status=status.HTTP_200_OK, data=res.json())

# Update delete get users


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage authenticated user"""
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrive and return authenticated user"""
        return self.request.user

    def patch(self, request):
        """Partially update user"""
        user = request.user
        serializer = self.serializer_class(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data="Profile has been updated")
        return Response(status=status.HTTP_400_BAD_REQUEST, data="Please check the update field")

# login/Register with facebook and google


class SocialLoginView(generics.GenericAPIView):
    """Log in using facebook and google"""
    serializer_class = serializers.SocialSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Authenticate user through the provider and access_token"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get('provider', None)
        strategy = load_strategy(request)
        # AppleIdAuth.TOKEN_TTL_SEC = timezone.now() + timedelta(days=180)

        try:
            backend = load_backend(strategy=strategy, name=provider,
                                   redirect_uri=None)

        except MissingBackend:
            return Response({'error': 'Please provide a valid provider'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            if isinstance(backend, BaseOAuth2):
                access_token = serializer.data.get('access_token')
                user = backend.do_auth(access_token)

        except HTTPError as error:
            return Response({
                "error": {
                    "access_token": "Invalid token",
                    "details": str(error)
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        except AuthTokenError as error:
            return Response({
                "error": "Invalid credentials",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            authenticated_user = backend.do_auth(access_token, user=user)

        except HTTPError as error:
            return Response({
                "error": "invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        except AuthForbidden as error:
            return Response({
                "error": "invalid token",
                "details": str(error)
            }, status=status.HTTP_403_FORBIDDEN)

        if authenticated_user and authenticated_user.is_active:
            login(request, authenticated_user)
            data = {
                "grant_type": "convert_token",
                "backend": provider,
                "token": serializer.data.get('access_token'),
                "client_id": os.environ.get('CLIENT_ID'),
                "client_secret": os.environ.get('CLIENT_SECRET')
            }
            if(settings.DEBUG):
                res = requests.post(
                    'http://127.0.0.1:8000/api/user/oauth/convert-token/',
                    json=data)
                return Response(status=status.HTTP_200_OK, data=res.json())
            else:
                res = requests.post(
                    'http://ec2-15-206-117-163.ap-south-1.compute.amazonaws.com/api/user/oauth/convert-token/',
                    json=data)
                return Response(status=status.HTTP_200_OK, data=res.json())


# upload profile pic or cover pic api
class UserImageUploadProfileView(generics.CreateAPIView):
    """Uploads image to user model"""
    serializer_class = UserImageUploadSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """Uploads image to user as profile image"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        image_url = serializer.data.get('image_url', None)
        image_type = serializer.data.get('image_type', None)

        image_temp_file = NamedTemporaryFile(delete=True)

        request = requests.get(image_url, stream=True,)
        if request.status_code != requests.codes.ok:
            return Response(status=status.HTTP_404_NOT_FOUND, data="File not found")
        file_name = image_url.split('/')[-1]
        image_temp_file.write(request.content)
        image_temp_file.flush()

        if image_type == 'profile':
            user.profile_photo_url.save(
                file_name, File(image_temp_file), save=True)
            user.save()
            return Response(status=status.HTTP_200_OK, data="Profile picture updated")
        if image_type == 'cover':

            user.cover_photo_url.save(
                file_name, File(image_temp_file), save=True)
            user.save()
            return Response(status=status.HTTP_200_OK, data="Cover photo updated")
        return Response(status=status.HTTP_400_BAD_REQUEST, data="Invalid image type")

# logout user


class LogoutView(generics.GenericAPIView):
    """Log out and revoke token"""
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """Revoke access token and logout user"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.data.get('token', None)

        if serializer.is_valid():
            data = {
                "token": token,
                "client_id": os.environ.get('CLIENT_ID'),
                "client_secret": os.environ.get('CLIENT_SECRET')
            }
            if(settings.DEBUG):
                res = requests.post(
                    'http://127.0.0.1:8000/api/user/oauth/revoke-token/',
                    json=data)
                request.user.is_active = False
                request.user.save()
                return Response(status=status.HTTP_200_OK, data="Successfully logged out.")
            else:
                res = requests.post(
                    'http://ec2-15-206-117-163.ap-south-1.compute.amazonaws.com/api/user/oauth/revoke-token/',
                    json=data)
            request.user.is_active = False
            request.user.save()
            return Response(status=status.HTTP_200_OK, data="Successfully logged out.")
        else:
            return Response(message="User not logged in",  status=status.HTTP_400_BAD_REQUEST)


# {"grant_type": "password", "username": "akieatos@gmail.com", "password": "123456", "client_id": "9752isO1cD3TBm1K9yVSAqb5pCuKD386fkIjiH", "client_secret": "tTJ6Z6TGOmut1AjUn2KniNWUx2l2IOjMjsW12azf7f2N0jx66A7DxbyodohsFfsxTFjkBaiY1ovnVVHLXSmXxEFvSyOfg4ybyOib4r92IRrmlfyuHi3bHyS4aM5StG"}
# def download_image(name, image, url):
#     input_file = StringIO(urlopen(url).read())
#     output_file = StringIO()
#     img = Image.open(input_file)
#     if img.mode != "RGB":
#         img = img.convert("RGB")
#     img.save(output_file, "JPEG")
#     image.save(name+".jpg", ContentFile(output_file.getvalue()), save=False ,)

# def get_remote_image(self):
#     if self.image_url and not self.image_file:
#         result = urllib.urlretrieve(self.image_url)
#         self.image_file.save(
#                 os.path.basename(self.image_url),
#                 File(open(result[0]))
#                 )
#         self.save()


# class GoogleLoginView(generics.GenericAPIView):
#     """Log in/Register using Google"""
#     serializer_class = serializers.SocialSerializer
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         """Authenticate user through the provider and access_token"""
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         provider = serializer.data.get('provider', None)
#         strategy = load_strategy(request)

#         try:
#             backend = load_backend(strategy=strategy, name=provider,
#                                    redirect_uri=None)

#         except MissingBackend:
#             return Response({'error': 'Please provide a valid provider'},
#                             status=status.HTTP_400_BAD_REQUEST)
#         try:
#             if isinstance(backend, BaseOAuth2):
#                 access_token = serializer.data.get('access_token')
#             # user = backend.do_auth(access_token)
#             user = backend.auth_complete(self)
#         except HTTPError as error:
#             return Response({
#                 "error": {
#                     "access_token": "Invalid token",
#                     "details": str(error)
#                 }
#             }, status=status.HTTP_400_BAD_REQUEST)
#         except AuthTokenError as error:
#             return Response({
#                 "error": "Invalid credentials",
#                 "details": str(error)
#             }, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             authenticated_user = backend.do_auth(access_token, user=user)

#         except HTTPError as error:
#             return Response({
#                 "error": "invalid token",
#                 "details": str(error)
#             }, status=status.HTTP_400_BAD_REQUEST)

#         except AuthForbidden as error:
#             return Response({
#                 "error": "invalid token",
#                 "details": str(error)
#             }, status=status.HTTP_400_BAD_REQUEST)

#         if authenticated_user and authenticated_user.is_active:
#             login(request, authenticated_user)
#             data = {
#                 'grant_type': 'convert_token',
#                 "backend": provider,
#                 'token': serializer.data.get('access_token'),
#                 'client_id': CLIENT_ID,
#                 'client_secret': CLIENT_SECRET,
#             }
#             res = requests.post(
#                 'http://127.0.0.1:8000/api/user/oauth/convert-token/',
#                 data)

#             return Response(status=status.HTTP_200_OK, data=res.json())


# {
#                "token":"RvWyKvoeUbdIjxgHuUnfr4ttPlAKjQ",
#                 "client_id": "dbp8ifqtMdZRgookFNQ9KBUnmiCqkxwnrvYLQ9Wv",
#                 "client_secret": "wv8I0XkOKSzGSUuwCfquxcd64A9Kpd3ibysRk5zcz7vS1RSaJ4or8LGTK2TcnZWVOmYcoLxZzT8hUaWOklG26Bm9GvNqVZI2lXEBwzSHmb3OlqmAKqBhLypMglm3yVtL"
#             }


# from django.core.files import File
# import os

# class Item(models.Model):
#     image_file = models.ImageField(upload_to='images')
#     image_url = models.URLField()

# ...

# def get_remote_image(self):
#     if self.image_url and not self.image_file:
#         result = urllib.urlretrieve(self.image_url)
#         self.image_file.save(
#                 os.path.basename(self.image_url),
#                 File(open(result[0]))
#                 )
#         self.save()


# class FbLogin(APIView):
#     authentication_classes = (authentication.TokenAuthentication,)
#     permission_classes = (permissions.AllowAny,)

#     @csrf_exempt
#     def dispatch(self, *args, **kwargs):
#         return super(FbLogin, self).dispatch(*args, **kwargs)

#     @staticmethod
#     def post(request):
#         request_data = JSONParser().parse(request)

#         if 'access_token' in request_data:
#             response = requests.get(
#                 url='https://graph.facebook.com/v2.5/me/',
#                 params={
#                     'access_token': request_data['access_token'],
#                     'fields': 'email,first_name,last_name',
#                 },
#             )

#             json_response = json.loads(response.text)

#             if 'error' not in json_response:
#                 response_photo = requests.get(
#                     url='https://graph.facebook.com/v2.5/%s/picture' % json_response['id'],
#                     params={
#                         'redirect': 'false',
#                         'type': 'large',
#                     },
#                 )
#                 response_photo_json = json.loads(response_photo.text)

#                 response_friends = requests.get(
#                     url='https://graph.facebook.com/v2.5/me/friends/',
#                     params={
#                         'access_token': request_data['access_token'],
#                         'limit': 300,
#                     },
#                 )

#                 generated_password = get_random_string(10, '0123456789abcdefghijklmnopqrstuvwxyz')
#                 try:
#                     json_response_email = json_response['email']
#                 except:
#                     first_name = json_response['first_name'].lower()
#                     last_name = json_response['last_name'].lower()
#                     id = json_response['id']
#                     json_response_email = first_name + last_name + id + '@facebook.com'
#                 try:
#                     current_user = User.objects.get(email=json_response_email)
#                     current_user.set_password(generated_password)
#                     current_user.save()
#                 except User.DoesNotExist:
#                     new_user = User.objects.create_user(email=json_response_email,
#                                                         password=generated_password)

#                     new_user.provider_id = json_response['id']
#                     new_user.provider_type = 'facebook'

#                     if 'first_name' in json_response:
#                         new_user.first_name = json_response['first_name']

#                     if 'last_name' in json_response:
#                         new_user.last_name = json_response['last_name']

#                     new_user.save()

#                     photo_name = urlparse(response_photo_json['data']['url']).path.split('/')[-1].split('?')[-1]
#                     photo_content = urllib.request.urlretrieve(response_photo_json['data']['url'])

#                     new_user.profile_photo.save(photo_name, File(open(photo_content[0], 'rb')), save=True)
#                 user = authenticate(email=json_response_email, password=generated_password)
#                 try:
#                     token = Token.objects.get(user=user)
#                 except Token.DoesNotExist:
#                     token = Token.objects.create(user=user)
#                 if user is not None:
#                     if user.is_active:
#                             fullname = json_response['first_name'] + ' ' + json_response['last_name']
#                             return JsonResponse({'result': 'success', 'token': token.key, 'name': fullname}, status=200)

#             return JsonResponse({'result': 'User access token is incorrect'}, status=400)
