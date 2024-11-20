# You shouldn't have to change anything in here, ever.
# Use settings.ini in the project's root directory instead.

# If you make any changes in here, you may have trouble updating your Kumify installation.

from pathlib import Path

from autosecretkey import AutoSecretKey

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = AutoSecretKey(BASE_DIR / "settings.ini")

SECRET_KEY = CONFIG_FILE.secret_key
DEBUG = CONFIG_FILE.config.getboolean("KUMIFY", "Debug", fallback=False)

ALLOWED_HOSTS = [CONFIG_FILE.config.get("KUMIFY", "Host")]
CSRF_TRUSTED_ORIGINS = [f"https://{ALLOWED_HOSTS[0]}"]

TIME_ZONE = CONFIG_FILE.config.get("KUMIFY", "TimeZone", fallback="UTC")

# Application definition

try:
    ENABLED_MODULES  # TODO: Move this to settings.ini
except NameError:
    ENABLED_MODULES = [
        "cbt",
        "mood",
        "dreams",
        "health",
        "friends",
        "habits",
        "gpslog",
    ]

CORE_MODULES = [
    "common",
    "frontend",
    "msgio",
    "cronhandler",
]

INSTALLED_APPS = (
    [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "colorfield",
        "multiselectfield",
        "dbsettings",
        "mozilla_django_oidc",
    ]
    + CORE_MODULES
    + ENABLED_MODULES
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "kumify.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "kumify.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if "MySQL" in CONFIG_FILE.config:
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.mysql",
            "NAME": CONFIG_FILE.config.get("MySQL", "Database"),
            "USER": CONFIG_FILE.config.get("MySQL", "Username"),
            "PASSWORD": CONFIG_FILE.config.get("MySQL", "Password"),
            "HOST": CONFIG_FILE.config.get("MySQL", "Host", fallback="localhost"),
            "PORT": CONFIG_FILE.config.getint("MySQL", "Port", fallback=3306),
            "OPTIONS": {
                "charset": "utf8mb4",
                "sql_mode": "traditional",
            },
        }
    }

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.spatialite",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

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

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = CONFIG_FILE.config.get(
    "KUMIFY", "StaticRoot", fallback=BASE_DIR / "static"
)

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

if "S3" in CONFIG_FILE.config:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"
    AWS_ACCESS_KEY_ID = CONFIG_FILE.config.get("S3", "AccessKey")
    AWS_SECRET_ACCESS_KEY = CONFIG_FILE.config.get("S3", "SecretKey")
    AWS_STORAGE_BUCKET_NAME = CONFIG_FILE.config.get("S3", "Bucket")
    AWS_S3_ENDPOINT_URL = CONFIG_FILE.config.get("S3", "Endpoint")


# OpenID Connect
# https://mozilla-django-oidc.readthedocs.io/

USE_OIDC = False

if "OIDC" in CONFIG_FILE.config:
    USE_OIDC = True

    OIDC_PROVIDER_NAME = CONFIG_FILE.config.get(
        "OIDC", "ProviderName", fallback="OpenID Connect"
    )

    AUTHENTICATION_BACKENDS.append("mozilla_django_oidc.auth.OIDCAuthenticationBackend")

    OIDC_RP_CLIENT_ID = CONFIG_FILE.config.get("OIDC", "ClientID")
    OIDC_RP_CLIENT_SECRET = CONFIG_FILE.config.get("OIDC", "ClientSecret")

    if opsk := CONFIG_FILE.config.get("OIDC", "OPSignKey", fallback=""):
        OIDC_RP_SIGN_ALGO = "RS256"
        OIDC_RP_IDP_SIGN_KEY = opsk
    elif jwks := CONFIG_FILE.config.get("OIDC", "JWKSEndpoint", fallback=""):
        OIDC_RP_SIGN_ALGO = "RS256"
        OIDC_OP_JWKS_ENDPOINT = jwks

    OIDC_OP_AUTHORIZATION_ENDPOINT = CONFIG_FILE.config.get(
        "OIDC", "AuthorizationEndpoint"
    )
    OIDC_OP_TOKEN_ENDPOINT = CONFIG_FILE.config.get("OIDC", "TokenEndpoint")
    OIDC_OP_USER_ENDPOINT = CONFIG_FILE.config.get("OIDC", "UserInfoEndpoint")

    OIDC_CREATE_USER = CONFIG_FILE.config.get("OIDC", "CreateUsers", fallback=False)
