import os
from django.utils import timezone
from datetime import timedelta
# import jwt

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", default=0))
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "admin_interface", # visit to change theme cmd to https://pypi.org/project/django-admin-interface/ for more info
    "colorfield",
    'rest_framework',
    'drf_yasg',
    'oauth2_provider',
    'social_django',
    'drf_social_oauth2',
    'storages',
    'core',
    'user',
    'vendor',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'drf_social_oauth2.authentication.SocialAuthentication',
    )
}



# The settings of AUTHENTICATION_BACKENDS app are:
# DRFSO2_PROPRIETARY_BACKEND_NAME: name of your OAuth2 social backend (e.g "Facebook"), defaults to "Django"
# DRFSO2_URL_NAMESPACE: namespace for reversing URLs
# ACTIVATE_JWT: If set to True the access and refresh tokens will be JWTed. Default is False.



#only if django version >= 3.0 django admin or visit https://pypi.org/project/django-admin-interface/
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880


AUTHENTICATION_BACKENDS = (

    'social_core.backends.apple.AppleIdAuth',



    # Facebook OAuth2
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    # Google OAuth2
    'social_core.backends.google.GoogleOAuth2',
    # 'social_core.backends.google.GoogleOpenId', #deprecated
    'social_core.backends.google_openidconnect.GoogleOpenIdConnect',
    'social_core.backends.google.GoogleOAuth',



    # django-rest-framework-social-oauth2
    'drf_social_oauth2.backends.DjangoOAuth2',

    # Django
    'django.contrib.auth.backends.ModelBackend',
)

# DRFSO2_PROPRIETARY_BACKEND_NAME="Django"
# DRFSO2_URL_NAMESPACE='0.0.0.0:8000'


TEAM = os.environ.get('APPLE_TEAM_ID')
KEY =os.environ.get('APPLE_SIGN_IN_APP_KEY')
CLIENT =os.environ.get('APPLE_SIGN_IN_CLIENT_ID')
# SECRET = """
# -----BEGIN PRIVATE KEY-----
# MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgt1xntTioixpSGKjE
# 17hLyv6Zu9vIGxd1RSUx2zQ6i+igCgYIKoZIzAATi9yePLapQjnLG
# zRq2R8pgE0/9XiK0UZUQC6sjXaRfpkE5dWavX81XyONOEIN452Bs/ILuYXabHsCX
# 7Sw1dEc3
# -----END PRIVATE KEY-----"""
SECRET= os.environ.get('APPLE_SIGN_IN_CLIENT_SECRET')

SCOPE = ['name', 'email']
EMAIL_AS_USERNAME = True


SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('FACEBOOK_APP_ID')
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('FACEBOOK_APP_SECRET')
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('GOOGLE_APP_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('GOOGLE_APP_SECRET')


SOCIAL_AUTH_APPLE_ID_SCOPE = ['email', 'name']
SOCIAL_AUTH_APPLE_ID_EMAIL_AS_USERNAME = True
# Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from facebook. Email is not sent by default, to get it, you must request the email permission:
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'}
FACEBOOK_EXTENDED_PERMISSIONS = ['email']


SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

# SOCIAL_AUTH_CLEAN_USERNAME_FUNCTION = 'unidecode.unidecode'
SOCIAL_AUTH_JSONFIELD_ENABLED = True

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details', )


# Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
# drf_social_oauth2 social auth scope
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

OAUTH2_PROVIDER = {
    # other OAUTH2 settings
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore'
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "Asia/Dhaka"

USE_I18N = True

USE_L10N = True

USE_TZ = True

AWS_DEFAULT_ACL = None


AUTH_USER_MODEL = 'core.User'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# STATIC_URL = '/static/'
# MEDIA_URL = '/media/'

# 127.0.0.1:8000/media


USE_S3 = os.getenv('USE_S3') == 'TRUE'

if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'app.storage_backends.StaticStorage'
    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'app.storage_backends.PublicMediaStorage'
else:
    STATIC_URL = '/staticfiles/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_URL = '/mediafiles/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')


# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "staticfiles"),
# ]

# {
# "client_id":"y5fXqx7nzaIMCJM1ZAHQafpYA06CXNfxbT769Sfw",
# "client_secret":"GD54vCrrL2QzptBECJ8N3zN7sX5AokAZw48Q2pKm540V5RbtdU1aEeWVEnFbMEy5utB035L8dx8pzJhGrPNotagmdVIe2yweuFsOTbtEjnRiRxVUbxzd2EatuDYFmTKA",
# "grant_type":"password",
# "username":"zuhabul.islam@gmail.com",
# "password":"asasxcxc12345"
# }
# curl -X POST -d "client_id=y5fXqx7nzaIMCJM1ZAHQafpYA06CXNfxbT769Sfw&client_secret=GD54vCrrL2QzptBECJ8N3zN7sX5AokAZw48Q2pKm540V5RbtdU1aEeWVEnFbMEy5utB035L8dx8pzJhGrPNotagmdVIe2yweuFsOTbtEjnRiRxVUbxzd2EatuDYFmTKA&grant_type=password&username=zuhabul.islam@gmail.com&password=asasxcxc12345" http://127.0.0.1/api/user/oauth/token

# curl -X POST -F "username=test1" -F "password=test1" http://127.0.0.1:8000/sign_up/

# curl -X POST -d "grant_type=client_credentials" -u "<client_id>:<client_secret>" http://127.0.0.1:8000/o/token/

# {
# "grant_type":"convert_token",
# "client_id":"dbp8ifqtMdZRgookFNQ9KBUnmiCqkxwnrvYLQ9Wv",
# "client_secret":"wv8I0XkOKSzGSUuwCfquxcd64A9Kpd3ibysRk5zcz7vS1RSaJ4or8LGTK2TcnZWVOmYcoLxZzT8hUaWOklG26Bm9GvNqVZI2lXEBwzSHmb3OlqmAKqBhLypMglm3yVtL",
# "backend":"facebook",
# "token":"EAAPPff822swBANUaKRHTFOFZArKSpkMd9aaI9DgkD6HEpum88wiz54faqqYoY5PDQWvrjYkIYrubY8gANHIhlXcaPwKJvmZCbxd1ASA6zfUZCj04wSZACjZBHmrPakEZC5StlQWZAm3EHz6zyCZB8PSoAEVgK4ox5CZBZBwmnKxvsZAkgZDZD"
# }
