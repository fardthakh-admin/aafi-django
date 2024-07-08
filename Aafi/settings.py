from pathlib import Path
import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-b24#+xxy#vf05zx8g+%@1p4p7iryx4uth0ulq(etw_vs54_&d!"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','portal.techcare.health', '146.190.233.238', 'localhost','10.0.2.2']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "api.apps.ApiConfig",
    "frontend.apps.FrontendConfig",
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'widget_tweaks',
    'ckeditor',
   
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'api.middleware.AdminOnlyMiddleware',

]

REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': (
     'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
    'rest_framework_simplejwt.authentication.JWTAuthentication', 
  ),
}

ROOT_URLCONF = "Aafi.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, 'templates'), 
            BASE_DIR / 'templates',  
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'frontend.context_processors.collections_processor'
            ],
        },
    },
]


WSGI_APPLICATION = "Aafi.wsgi.application"


DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": "aafi",
        "USER": "postgres",
        "PASSWORD": "1234",
        "HOST": "localhost",
        "PORT": "5432",
    }
    #  "default": {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     "NAME": "railway",
    #     "USER": "postgres",
    #     "PASSWORD": "dCyRjRSEXHUyYwpjdEdJqWOLSdqmpuUI",
    #     "HOST": "viaduct.proxy.rlwy.net",
    #     "PORT": "32989",
    # }
    #      'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'aafi',
    #     'USER': 'root',
    #     'PASSWORD': '',
    #     'HOST': 'localhost', 
    #     'PORT': '3306',      
    # }

}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Amman"

USE_I18N = True

USE_TZ = True


AUTH_USER_MODEL = "api.User"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = "/static/"
# MEDIA_URL = '/images/'
# STATIC_ROOT = os.path.join(BASE_DIR, '/static/')

# STATICFILES_DIRS = [
#     BASE_DIR / 'static'
# ]

# MEDIA_ROOT = BASE_DIR / 'static/images'

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')  # Ensure this is a separate directory

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')  # This should be where your development static files are located
]

MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ORIGIN_ALLOW_ALL = True # ALLOWS ALL FRONTEND PORTS TO ACCESS OUR APP
CORS_ALLOW_CREDENTIALS = True # ALLOWS FRONTEND TO GET COOKIE

cred = credentials.Certificate("techcare-diabetes-firebase-adminsdk-i6cxk-c8c54ebaf3.json")
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "techcare-diabetes-firebase-adminsdk-i6cxk-c8c54ebaf3.json"


CSRF_TRUSTED_ORIGINS = ['https://72a8-109-107-231-24.ngrok-free.app']



SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',    
}

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8080',
]
