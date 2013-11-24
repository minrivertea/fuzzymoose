# Django settings for fuzzy project.
import os
PROJECT_PATH = os.path.normpath(os.path.dirname(__file__))

# BASIC SETTINGS
# -------------------------------------------------------

DEBUG =                             False
GA_IS_ON =                          True
TEMPLATE_DEBUG =                    DEBUG
ADMINS =                            (('Chris West', 'chris@minrivertea.com'),)
MANAGERS = ADMINS
ALLOWED_HOSTS =                     ['www.fuzzymoose.co.uk',]                                   
TIME_ZONE =                         'America/Chicago'
LANGUAGE_CODE =                     'en-gb'
SITE_ID =                           1
USE_I18N =                          False
USE_L10N =                          False
USE_TZ =                            True
SECRET_KEY =                        'n1!^f&amp;@l01zfj@uq)%akb3l(#%!6ee6woe$%j^9b#dul_+sm&amp;9'
ROOT_URLCONF =                      'fuzzy.urls'
WSGI_APPLICATION =                  'fuzzy.wsgi.application'
ANALYTICS_ID =                      ''
SITE_NAME =                         'FuzzyMoose'
SITE_URL =                          'http://www.fuzzymoose.co.uk'
SITE_DOMAIN =                       'www.fuzzymoose.co.uk'
SITE_EMAIL =                        'Angelique <info@fuzzymoose.co.uk>'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'fuzzymoose',                      
        'USER': '',                      
        'PASSWORD': '',                  
        'HOST': '',                      
        'PORT': '',                      
    }
}


# MEDIA AND STATIC SETTINGS
# -------------------------------------------------------

MEDIA_ROOT =                        os.path.join(PROJECT_PATH, 'media')
MEDIA_URL =                         '/media/'
STATIC_ROOT =                       os.path.join(PROJECT_PATH, 'static')
STATIC_URL =                        '/static/'
STATICFILES_DIRS = (

)
STATICFILES_FINDERS = (
                                    'django.contrib.staticfiles.finders.FileSystemFinder',
                                    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#                                    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# TEMPLATE SETTINGS
# -------------------------------------------------------

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
    os.path.join(PROJECT_PATH, 'shop/templates')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'fuzzy.shop.context_processors.common',
    'django.contrib.messages.context_processors.messages',
)

BASE_TEMPLATE =                     'base.html'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'fuzzy.shop',
    'fuzzy.blog',
    'captcha',
    'sorl.thumbnail',
    'ckeditor',
    'south',
    'paintstore',
    
)

# PAYPAL SETTINGS
# -------------------------------------------------------
PAYPAL_RECEIVER_EMAIL =             'chris@minrivertea.com'
PAYPAL_RETURN_URL =                 ''
PAYPAL_NOTIFY_URL =                 ''
PAYPAL_BUSINESS_NAME =              ''
PAYPAL_SUBMIT_URL =                 ''


# THUMBNAIL SETTINGS
# -------------------------------------------------------
THUMBNAIL_PRODUCT_PHOTO_LARGE =     '500x331'
THUMBNAIL_PRODUCT_PHOTO_MEDIUM =    '300x210'
THUMBNAIL_PRODUCT_PHOTO_SMALL =     '60x60'



# CKEDITOR SETTINGS
# -------------------------------------------------------
CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'ckuploads')
CKEDITOR_UPLOAD_PREFIX = "/media/ckuploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            [      'Undo', 'Redo',
              '-', 'Bold', 'Italic', 'Underline', 'BulletedList', 'NumberedList', 'Image',
              '-', 'Link', 'Unlink', 'Anchor',
              '-', 'Format',
              '-', 'PasteFromWord',
              '-', 'Maximize', 'Source', 
            ],
        ],
        'width': 840,
        'height': 300,
        'toolbarCanCollapse': False,
    }
}


# MAIL SETTINGS
# -------------------------------------------------------
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_PORT = ''


# INTERNATIONAL SETTINGS
# -------------------------------------------------------
LANGUAGE_COOKIE_NAME = ''
IPINFO_APIKEY = ''

try:
    from local_settings import *
except:
    pass





LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
