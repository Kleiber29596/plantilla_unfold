from pathlib        import Path
from datetime       import timedelta
from django.conf    import settings
from decouple       import config, Csv
import os

import datetime
import logging.config
import os


BASE_DIR            = Path(__file__).resolve().parent.parent
SECRET_KEY          = config('SECRET_KEY')
DEBUG               = config('DEBUG')
ALLOWED_HOSTS       = config('ALLOWED_HOSTS', cast=Csv())


BASE_APPS   =   [
                    'jazzmin',
                    'django.contrib.admin',
                    'django.contrib.auth',
                    'django.contrib.contenttypes',
                    'django.contrib.sessions',
                    'django.contrib.messages',
                    'django.contrib.staticfiles',
                    'simple_history',
                ]

LOCAL_APPS  =   [
                    'apps.cuenta',
                    'apps.frontend',
                    'apps.auxiliares',
                    'apps.gestion',
                    'apps.historico'

                ]

THIRD_APPS =    [
                    'corsheaders',
                    'ninja_extra',
                    'ninja_jwt',
                    'django_rest_passwordreset',
                    'import_export',
                    'smart_selects',
                    #'maintenance_mode',
                ]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS


MIDDLEWARE      =   [
                        'django.middleware.security.SecurityMiddleware',
                        'django.contrib.sessions.middleware.SessionMiddleware',
                        # Incluida
                        "corsheaders.middleware.CorsMiddleware",
                        'django.middleware.common.CommonMiddleware',
                        'django.middleware.csrf.CsrfViewMiddleware',
                        'django.contrib.auth.middleware.AuthenticationMiddleware',
                        'django.contrib.messages.middleware.MessageMiddleware',
                        'django.middleware.clickjacking.XFrameOptionsMiddleware',
                        #'maintenance_mode.middleware.MaintenanceModeMiddleware',
                    ]

ROOT_URLCONF    =   'configuracion.urls'

TEMPLATES       =   [
                        {
                            'BACKEND'   :   'django.template.backends.django.DjangoTemplates',
                            'DIRS'      :   [os.path.join(BASE_DIR, 'templates')],
                            'APP_DIRS'  :   True,
                            'OPTIONS'   :   {
                                                'context_processors': 
                                                [
                                                    'django.template.context_processors.debug',
                                                    'django.template.context_processors.request',
                                                    'django.contrib.auth.context_processors.auth',
                                                    'django.contrib.messages.context_processors.messages',
                                                ],
                                            },
                        },
                    ]

WSGI_APPLICATION = 'configuracion.wsgi.application'


DATABASES = {
                'default' :     {
                                    'ENGINE':           'django.db.backends.postgresql',
                                    'NAME':             config('BD_PRINCIPAL'),
                                    'USER':             config('USUARIO_DESARROLLO'),
                                    'PASSWORD':         config('CLAVE_DESARROLLO'),
                                    'HOST':             config('IP_DESARROLLO'),
                                    'PORT':             config('PUERTO_PREDETERMINADO'),
                                    #"ATOMIC_REQUESTS":  config('ATOMIC_REQUESTS'),
                                    # PARA LEER CON InspectDB un esquema especifico
                                    #'OPTIONS': {'options': '-c search_path=cuenta'}
                                    ## Para leer con InspectDB un esquema especifico
                                    #'OPTIONS': {'options': '-c search_path=censo'}
                                },
            }

AUTH_USER_MODEL             = 'cuenta.User'
AUTH_PASSWORD_VALIDATORS =  [
                                { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',   },
                                { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',             },
                                { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',            },
                                { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',           },
                            ]


LANGUAGE_CODE       = 'es-ve'
TIME_ZONE           = 'America/Caracas'
USE_I18N            = True
USE_TZ              = True
DEFAULT_AUTO_FIELD  = 'django.db.models.BigAutoField'

STATIC_URL          = 'static/'
STATICFILES_DIRS    = [os.path.join(BASE_DIR, 'static/'),]
STATIC_ROOT         = os.path.join(BASE_DIR, 'staticfiles/')
MEDIA_ROOT          = os.path.join(BASE_DIR, 'media/')
MEDIA_URL           = '/media/'


CORS_ALLOW_ALL_ORIGINS          =   True
'''
CORS_ALLOWED_ORIGINS =  [
                            "https://example.com",
                        ]
'''
AUTH_USER_MODEL     = 'cuenta.User'

DATABASE_ROUTERS    =   (
                            #'conexiones.nomina_mppe.PersonalMPPE_DBRouter',
                            #'conexiones.nomina_entes.PersonalEnte_DBRouter',
                            
                            #'conexiones.geo_estado.Estado_DBRouter',
                            #'conexiones.geo_municipio.Municipio_DBRouter',
                            #'conexiones.geo_parroquia.Parroquia_DBRouter',
                            #'conexiones.geo_comunidad.Comunidad_DBRouter',

                            #'conexiones.gescolar_plantel.Plantel_DBRouter',

                            #'conexiones.saime.Saime_DBRouter',
                        )

# Logging Configuration

# Clear prev config
LOGGING_CONFIG = None

# Get log_level from env
LOG_LEVEL = os.getenv("DJANGO_LOG_LEVEL", "info").upper()

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters":   {
                            "console":  {
                                            "format": "%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %("
                                            "message)s",
                                        },
                        },
        "handlers":     {
                            "console": 
                                        {
                                            "class": "logging.StreamHandler",
                                            "formatter": "console",
                                        },
                        },
        "loggers":      {
                            "":         {
                                            "level": LOG_LEVEL,
                                            "handlers": ["console",],
                                        },
                        },
    }
)

# Configuracion del SWagger
SWAGGER_SETTINGS =  {
                        "USE_SESSION_AUTH": False,
                        "api_version":      "0.1",
                        "SECURITY_DEFINITIONS": {"api_key": {"type": "apiKey", "name": "Authorization", "in": "header"},},
                    }

# Configuracion de CELERY
REDIS_URL                       =   os.getenv("BROKER_URL", "redis://localhost:6379")
CELERY_BROKER_URL               =   REDIS_URL
CELERY_BROKER_TRANSPORT_OPTIONS =   {
                                        "visibility_timeout": 3600,  # 1 hour
                                    }
CELERY_ACCEPT_CONTENT           =   ["application/json"]
CELERY_TASK_SERIALIZER          =   "json"
CELERY_RESULT_SERIALIZER        =   "json"
CELERY_TIMEZONE                 =   TIME_ZONE


#NINJA_JWT                       = {'TOKEN_OBTAIN_PAIR_INPUT_SCHEMA': 'apps.cuenta.views.token.MyTokenObtainPairInputSchema',}
# Configuracion del uso de JWT
NINJA_JWT                       =   {
                                        'ACCESS_TOKEN_LIFETIME':    timedelta(minutes=5),
                                        'REFRESH_TOKEN_LIFETIME':   timedelta(days=1),
                                        'ROTATE_REFRESH_TOKENS':    False,
                                        'BLACKLIST_AFTER_ROTATION': False,
                                        'UPDATE_LAST_LOGIN':        False,

                                        'ALGORITHM':                'HS256',
                                        'SIGNING_KEY':              config('SECRET_KEY'),
                                        'VERIFYING_KEY':            None,
                                        'AUDIENCE':                 None,
                                        'ISSUER':                   None,
                                        'JWK_URL':                  None,
                                        'LEEWAY':                   0,

                                        'USER_ID_FIELD':            'id',
                                        'USER_ID_CLAIM':            'user_id',
                                        'USER_AUTHENTICATION_RULE': 'ninja_jwt.authentication.default_user_authentication_rule',

                                        'AUTH_TOKEN_CLASSES':       ('ninja_jwt.tokens.AccessToken',),
                                        'TOKEN_TYPE_CLAIM':         'token_type',
                                        'TOKEN_USER_CLASS':         'ninja_jwt.models.TokenUser',

                                        'JTI_CLAIM':                        'jti',

                                        'SLIDING_TOKEN_REFRESH_EXP_CLAIM':  'refresh_exp',
                                        'SLIDING_TOKEN_LIFETIME':           timedelta(minutes=5),
                                        'SLIDING_TOKEN_REFRESH_LIFETIME':   timedelta(days=1),

                                        # For Controller Schemas
                                        # FOR OBTAIN PAIR
                                        'TOKEN_OBTAIN_PAIR_INPUT_SCHEMA':           "ninja_jwt.schema.TokenObtainPairInputSchema",
                                        'TOKEN_OBTAIN_PAIR_REFRESH_INPUT_SCHEMA':   "ninja_jwt.schema.TokenRefreshInputSchema",
                                        # FOR SLIDING TOKEN
                                        'TOKEN_OBTAIN_SLIDING_INPUT_SCHEMA':        "ninja_jwt.schema.TokenObtainSlidingInputSchema",
                                        'TOKEN_OBTAIN_SLIDING_REFRESH_INPUT_SCHEMA':"ninja_jwt.schema.TokenRefreshSlidingInputSchema",

                                        'TOKEN_BLACKLIST_INPUT_SCHEMA':             "ninja_jwt.schema.TokenBlacklistInputSchema",
                                        'TOKEN_VERIFY_INPUT_SCHEMA':                "ninja_jwt.schema.TokenVerifyInputSchema",
                                    }


JAZZMIN_SETTINGS = {
                        # title of the window (Will default to current_admin_site.site_title if absent or None)
                        "site_title": "Admin",

                        # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
                        "site_header": "SIA-OTIC",

                        # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
                        "site_brand": "SIA-OTIC",

                        # Logo to use for your site, must be present in static files, used for brand on top left
                        "site_logo": "img/logomppe.png",
                        "login_logo": "img/logomppe.png",

                        # CSS classes that are applied to the logo above
                        "site_logo_classes": "img-circle",

                        # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
                        "site_icon": None,

                        # Welcome text on the login screen
                        "welcome_sign": "Bienvenido al Sistema de Gestion de Inventario",

                        # Copyright on the footer
                        "copyright": "Oficina de Tecnologías de la Información y la Comunicación (OTIC) Ministerio del Poder Popular para la Educación R.I.F.: G-20000009-0",

                        # The model admin to search from the search bar, search bar omitted if excluded
                        #"search_model": "auth.User",

                        # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
                        "user_avatar": None,

                        ############
                        # Top Menu #
                        ############

                        # Links to put along the top menu
                        "topmenu_links": [
                                            # Url that gets reversed (Permissions can be added)
                                            {"name": "Inicio",  "url": "admin:index", "permissions": ["auth.view_user"]},
                                            # external url that opens in a new window (Permissions can be added)
                                            {"name": "Reporte General",       "url": "/reporte-general/",  "new_window": True},

                                            {"name": "Activar Mantenimiento",       "url": "/maintenance-mode/on/",  "new_window": True},
                                            {"name": "Desactivar Mantenimiento",    "url": "/maintenance-mode/off/", "new_window": True},

                                            # model admin to link to (Permissions checked against model)
                                            #{"model": "auth.User"},

                                            # App with dropdown menu to all its models pages (Permissions checked against models)
                                            #{"app": "apps.nomina"},
                                        ],

                        #############
                        # User Menu #
                        #############

                        # Additional links to include in the user menu on the top right ("app" url type is not allowed)
                        "usermenu_links":   [
                                                #{"name": "Desactivar mantenimiento",    "url": "/maintenance-mode/off/", "new_window": True},
                                                #{"name": "Activar Mantenimiento",       "url": "/maintenance-mode/non/", "new_window": True},
                                                {"model": "auth.user"}
                                            ],

                        #############
                        # Side Menu #
                        #############

                        # Whether to display the side menu
                        "show_sidebar": True,

                        # Whether to aut expand the menu
                        "navigation_expanded": True,

                        # Hide these apps when generating side menu e.g (auth)
                        "hide_apps":    [
                                            #'token_blacklist',
                                            #'auth'
                                            'token_blacklist'
                                        ],

                        # Hide these models when generating side menu (e.g auth.user)
                        "hide_models":  [
                                            'django_rest_passwordreset.resetpasswordtoken',
                                            # 'gestion.inventario',
                                            'auxiliares.responsable',
                                            'gestion.director'
                                        ],

                        # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
                        "order_with_respect_to":    [
                                                      
                                                        # 'visitas',
                                                        # 'users',
                                                        
                                                        'cuenta',
                                                        'auth',
                                                        'gestion',
                                                        'auxiliares',
                                                        'historico',
                                                          
                                                       
                                                    ],

                        # Custom links to append to app groups, keyed on app name
                        "custom_links": {    
                                            #"historico":    [{"name": "Nombre del Link", "url": "ruta", "icon": "fas fa-comments", "permissions": ["app.permiso"]}]
                                            "gestion": [
                                            {"name": "Responsables", "url": "/admin/auxiliares/responsable/", "icon": "fas fa-users"},
                                          
                                             ],       
                                        },

                        # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
                        # for the full list of 5.13.0 free icon classes
                        
                        "icons":    {
                                        "auth":                     "fas fa-users-cog",
                                        "cuenta.user":              "fa-solid fa-users",
                                        "auth.group":               "fa-solid fa-users-viewfinder",
                                        "gestion.inventario":       "fa-solid fa-pallet"
                                    },
                        # Icons that are used when one is not manually specified
                        "default_icon_parents":     "fas fa-chevron-circle-right",
                        "default_icon_children":    "fas fa-circle",

                        #################
                        # Related Modal #
                        #################
                        # Use modals instead of popups
                        "related_modal_active": False,

                        #############
                        # UI Tweaks #
                        #############
                        # Relative paths to custom CSS/JS scripts (must be present in static files)
                        "custom_css": None,
                        "custom_js": None,
                        # Whether to show the UI customizer on the sidebar
                        "show_ui_builder": False,

                        ###############
                        # Change view #
                        ###############
                        # Render out the change view as a single form, or in tabs, current options are
                        # - single
                        # - horizontal_tabs (default)
                        # - vertical_tabs
                        # - collapsible
                        # - carousel
                        "changeform_format": "horizontal_tabs",
                        # override change forms on a per modeladmin basis
                        "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
                        # Add a language dropdown into the admin
                        "language_chooser": False,
                    }
