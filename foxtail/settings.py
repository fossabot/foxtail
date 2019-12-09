"""
Base settings for the foxtail project.
You shouldn't need to edit this file in most cases.

Custom/instance specific settings can be customised using a
<.env> file placed in the project root, or with environment
variables (see https://django-environ.readthedocs.io/)

For Django documentation on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import logging
from pathlib import Path

import environ
import pymdownx.emoji
from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)

# Build paths inside the project like this: str(BASE_DIR / 'subdir').
BASE_DIR = Path(__file__).resolve(strict=True).parents[1]

env = environ.Env()
environ.Env.read_env(str(BASE_DIR / '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

SITE_URL = env('SITE_URL')
SITE_ID = 1

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
INTERNAL_IPS = env.list('INTERNAL_IPS', default=[])

ROOT_URLCONF = 'foxtail.urls'

WSGI_APPLICATION = 'foxtail.wsgi.application'

# Application definition
INSTALLED_APPS = [
    'apps.admin.apps.CustomAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.postgres',
    'django.contrib.sitemaps',
    'apps.core',
    'apps.accounts',
    'apps.content',
    'apps.events',
    'apps.directory',
    'foxtail_blog',
    'foxtail_contact',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.discord',
    'allauth.socialaccount.providers.github',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',
    'mail_templated_simple',
    'allauth_2fa',
    'taggit',
    'adminsortable2',
    'guardian',
    'webpack_loader',
    'crispy_forms',
    'oidc_provider',
    'captcha',
    'versatileimagefield',
    "django_rq",
    'django_cleanup.apps.CleanupConfig'
]

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'allauth_2fa.middleware.AllauthTwoFactorMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'oidc_provider.middleware.SessionManagementMiddleware',
]

if DEBUG:
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

# Template Engine
# <https://docs.djangoproject.com/en/dev/topics/templates/>

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR / 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'apps.core.context_processors.site',
                'csp.context_processors.nonce'
            ],
        },
    },
]

# Recognise upstream proxy SSL
# <https://docs.djangoproject.com/en/2.2/ref/settings/#secure-proxy-ssl-header>
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Database
# <https://docs.djangoproject.com/en/2.2/ref/settings/#databases>

DATABASES = {
    'default': env.db(
        'DATABASE_URL',
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3')
    )
}

# Cache
# <https://docs.djangoproject.com/en/2.2/topics/cache/#setting-up-the-cache>
CACHES = {
    'default': env.cache(default='dummycache://')
}

# enable the cached session backend
# <https://docs.djangoproject.com/en/2.2/topics/http/sessions/#using-cached-sessions>
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

# django-rq
# <https://github.com/rq/django-rq>
RQ_ASYNC = env.bool('RQ_ASYNC', default=True)

RQ_QUEUES = {
    'default': {
        'USE_REDIS_CACHE': 'default',
        'ASYNC': RQ_ASYNC
    }
}

# Authentication
# <https://django-allauth.readthedocs.io/en/latest/>

AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend'
]

ACCOUNT_ADAPTER = 'apps.accounts.authentication.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'apps.accounts.authentication.SocialAccountAdapter'

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

# custom validator allows spaces in usernames
ACCOUNT_USERNAME_VALIDATORS = 'apps.accounts.validators.username_validators'

LOGIN_REDIRECT_URL = '/'

ACCOUNT_FORMS = {
    'signup': 'apps.accounts.forms.SignupForm',
    'reset_password': 'apps.accounts.forms.ResetPasswordForm',
    'login': 'apps.accounts.forms.LoginForm'
}

ALLAUTH_2FA_ALWAYS_REVEAL_BACKUP_TOKENS = False

SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'read:user',
            'user:email'
        ],
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# Passwords
# <https://docs.djangoproject.com/en/2.2/topics/auth/passwords/>

# <https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators>
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# OIDC Server
# <https://django-oidc-provider.readthedocs.io/en/latest/>
OIDC_SESSION_MANAGEMENT_ENABLE = True
OIDC_USERINFO = 'apps.accounts.claims.userinfo'

OIDC_CLAIMS_SUPPORTED = [
    'sub',
    'name',
    'preferred_username',
    'nickname',
    'gender',
    'birthdate',
    'email',
    'email_verified'
]

# ReCAPTCHA
# <https://pypi.org/project/django-recaptcha/>
RECAPTCHA_ENABLED = True
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY')

# Taggit
# <https://django-taggit.readthedocs.io/en/latest/getting_started.html>
TAGGIT_CASE_INSENSITIVE = True

# Internationalization
# <https://docs.djangoproject.com/en/2.2/topics/i18n/>

LANGUAGE_CODE = 'en-au'
TIME_ZONE = 'Pacific/Auckland'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Static files and media (CSS, JavaScript, Images)
# <https://docs.djangoproject.com/en/2.2/howto/static-files/>
# <https://docs.djangoproject.com/en/dev/ref/settings/#media-root>

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# noinspection PyUnresolvedReferences
STATICFILES_DIRS = [
    ("bundles", str(BASE_DIR / 'assets/bundles')),
    str(BASE_DIR / 'assets/static')
]

AZURE_ENABLED = env.bool('AZURE_ENABLED', default=False)

if AZURE_ENABLED:

    AZURE_ACCOUNT_NAME = env('AZURE_ACCOUNT_NAME')
    AZURE_ACCOUNT_KEY = env('AZURE_ACCOUNT_KEY')
    AZURE_CUSTOM_DOMAIN = env('AZURE_CUSTOM_DOMAIN', default=None)

    AZURE_SSL = env.bool('AZURE_SSL', default=True)
    AZURE_EMULATED_MODE = env.bool('AZURE_EMULATED_MODE', default=False)

    AZURE_MEDIA_CONTAINER = env('AZURE_MEDIA_CONTAINER')
    AZURE_STATIC_CONTAINER = env('AZURE_STATIC_CONTAINER')

    DEFAULT_FILE_STORAGE = 'apps.core.storages.MediaAzureStorage'
    STATICFILES_STORAGE = 'apps.core.storages.StaticAzureStorage'

else:
    MEDIA_ROOT = str(BASE_DIR / 'media')
    STATIC_ROOT = str(BASE_DIR / 'static_out')


# if using the debug server, set the correct MIME type for .js files
if DEBUG:
    import mimetypes
    mimetypes.add_type("text/javascript", ".js", True)

# Webpack Loader
# <https://github.com/owais/django-webpack-loader>
WEBPACK_STATS_PATH = env('WEBPACK_STATS_PATH', default='webpack-stats.json')

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'bundles/',  # must end with slash
        'STATS_FILE': str(BASE_DIR / WEBPACK_STATS_PATH),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map']
    }
}

# Security
# <https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/#https>
# <https://docs.djangoproject.com/en/2.2/ref/middleware/#x-xss-protection>

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_NAME = '__Host-sessionid'

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_NAME = '__Host-csrftoken'

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = 'same-origin'

X_FRAME_OPTIONS = 'DENY'

# CSP Headers
# <https://django-csp.readthedocs.io/en/latest/>

CSP_INCLUDE_NONCE_IN = ['script-src', 'style-src']
CSP_UPGRADE_INSECURE_REQUESTS = True

ASSET_HOSTS = env.list('ASSET_HOSTS', default=[])

CSP_DEFAULT_SRC = ["'self'"]

CSP_REPORT_URI = env('CSP_REPORT_URI', default=None)

CSP_SCRIPT_SRC = ["'unsafe-inline'", "'self'", 'https://www.google.com/recaptcha/',
                  'https://www.gstatic.com/recaptcha/'] + ASSET_HOSTS
CSP_STYLE_SRC = ["'unsafe-inline'", 'fonts.googleapis.com', "'self'"] + ASSET_HOSTS
CSP_FRAME_SRC = ['https://www.google.com/recaptcha/']
CSP_FONT_SRC = ["'self'", 'data:', 'fonts.gstatic.com'] + ASSET_HOSTS
CSP_IMG_SRC = ["'self'", 'data:', 'ui-avatars.com', '*.wp.com', 'www.gravatar.com'] + ASSET_HOSTS
CSP_OBJECT_SRC = ["'none'"]
CSP_CONNECT_SRC = ["'self'", 'https://sentry.io']

CSP_BASE_URI = ["'none'"]
CSP_FRAME_ANCESTORS = ["'none'"]
CSP_FORM_ACTION = ["'self'"] + env.list('CSP_FORM_ACTION', default=[])

CSP_EXCLUDE_URL_PREFIXES = ('/admin',)

# we don't use strict-dynamic in debug because it breaks django-debug-toolbar
if not DEBUG:
    CSP_SCRIPT_SRC += ["'strict-dynamic'"]

# Sentry.io
# <https://docs.sentry.io/platforms/python/django/>

SENTRY_ENABLED = env.bool('SENTRY_ENABLED', default=False)

if SENTRY_ENABLED:
    SENTRY_DSN = env('SENTRY_DSN')

    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    _vars = {
        'dsn': SENTRY_DSN,
        'send_default_pii': env.bool('SENTRY_PII', default=False),
        'integrations': [DjangoIntegration()]
    }

    SENTRY_ENVIRONMENT = env('sentry_environment', default=False)

    if SENTRY_ENVIRONMENT:
        _vars['environment'] = SENTRY_ENVIRONMENT

    if env.bool('SENTRY_GIT', default=False):
        import git

        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha

        _vars['release'] = sha

        repo.close()

    sentry_sdk.init(**_vars)

# Logging
# <https://docs.djangoproject.com/en/dev/ref/settings/#logging>
# <https://docs.djangoproject.com/en/dev/topics/logging>
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] [%(process)d] [%(levelname)s] (%(module)s) %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "sentry_sdk": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# Email
# <https://docs.djangoproject.com/en/2.2/topics/email/>
DEFAULT_FROM_EMAIL = env('EMAIL_FROM_USER', default='webmaster@localhost')
SERVER_EMAIL = env('EMAIL_FROM_SYSTEM', default='root@localhost')

EMAIL_CONFIG = env.email_url('EMAIL_URL', default='consolemail://')

if RQ_ASYNC:
    EMAIL_REAL_BACKEND = EMAIL_CONFIG.get('EMAIL_BACKEND')
    EMAIL_CONFIG['EMAIL_BACKEND'] = 'apps.core.email.AsyncEmailBackend'

vars().update(EMAIL_CONFIG)


# Crispy Forms
# <https://django-crispy-forms.readthedocs.io/en/latest/>
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# VersatileImageField
# <https://django-versatileimagefield.readthedocs.io/en/latest/installation.html#versatileimagefield-settings>
VERSATILEIMAGEFIELD_SETTINGS = {
    'jpeg_resize_quality': 80,
    'cache_name': 'vif',
    'sized_directory_name': '_s',
    'filtered_directory_name': '_f'
}

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    'event_image': [
        ('mini', 'crop__350x175'),
        ('mini2x', 'crop__700x350'),
        ('banner', 'crop__1150x300'),
        ('admin', 'thumbnail__300x300')
    ],
    'post_image': [
        ('mini', 'crop__350x175'),
        ('mini2x', 'crop__700x350'),
        ('banner', 'crop__800x350'),
        ('banner2x', 'crop__1200x525'),
        ('admin', 'thumbnail__300x300')
    ]
}

# Markdown
MARKDOWN_EXTENSIONS = [
    'pymdownx.smartsymbols',
    'pymdownx.betterem',
    'pymdownx.tilde',
    'pymdownx.caret',
    'pymdownx.emoji',
    'sane_lists',
    'def_list',
    'nl2br',
    'abbr',
    'smarty'
]

MARKDOWN_EXTENSION_CONFIGS = {
    'pymdownx.emoji': {
        'emoji_generator': pymdownx.emoji.to_alt
    }
}

# Foxtail Blog
# <https://github.com/dmptrluke/foxtail-blog>

BLOG_COMMENTS = True

# Foxtail Contact
# <https://github.com/dmptrluke/foxtail-contact>

CONTACT_EMAILS = env.list('CONTACT_EMAILS')

# Heroku Support
if env.bool('USING_HEROKU', default=False):
    import django_heroku
    django_heroku.settings(locals())
