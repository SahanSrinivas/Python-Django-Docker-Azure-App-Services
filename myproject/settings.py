from pathlib import Path
import os
import re

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Get environment variables from Azure App Service configuration
AZURE_CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
AZURE_TENANT_ID = os.environ.get("AZURE_TENANT_ID")
AZURE_CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
AZURE_KEY_VAULT_NAME = os.environ.get("AZURE_KEY_VAULT_NAME")

# Use KeyVault if credentials are available, otherwise use environment variables directly
connection_string = None

if all([AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET, AZURE_KEY_VAULT_NAME]):
    try:
        from azure.identity import ClientSecretCredential
        from azure.keyvault.secrets import SecretClient
        
        KEY_VAULT_URI = f"https://{AZURE_KEY_VAULT_NAME}.vault.azure.net"
        
        # Authenticate using Service Principal
        credential = ClientSecretCredential(AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET)
        client = SecretClient(vault_url=KEY_VAULT_URI, credential=credential)
        
        # Get connection string from KeyVault
        connection_string = client.get_secret("azure-sql-connectionstring").value
        #print("✅ Successfully retrieved secret from Key Vault")
    except Exception as e:
        #print("❌ Error retrieving secret from KeyVault:", e)
        connection_string = None

# If KeyVault retrieval failed, try to get connection string from App Service Connection Strings
if not connection_string:
    connection_string = os.environ.get('SQLCONNSTR_Azure_Connection_String')
    if connection_string:
        print("✅ Using connection string from App Service Connection Strings")
    else:
        print("❌ No connection string available")

# SECURITY WARNING: keep the secret key used in production secret!
# Try to get SECRET_KEY from environment variable, fall back to a default if not available
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Get allowed hosts from environment variable or use defaults
ALLOWED_HOSTS_ENV = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = ALLOWED_HOSTS_ENV.split(',') if ALLOWED_HOSTS_ENV else ['testdockerazure.azurewebsites.net', 'localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS_ENV = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
CSRF_TRUSTED_ORIGINS = CSRF_TRUSTED_ORIGINS_ENV.split(',') if CSRF_TRUSTED_ORIGINS_ENV else ['https://testdockerazure.azurewebsites.net']

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# Database configuration
def parse_connection_string(conn_str):
    params = {}
    
    # Extract DRIVER correctly
    driver_match = re.search(r'DRIVER=\{(.*?)\}', conn_str)
    if driver_match:
        params['driver'] = driver_match.group(1)
    
    # Process remaining parameters
    for param in conn_str.split(";"):
        if "=" in param and not param.startswith("DRIVER"):
            key, value = param.split("=", 1)
            params[key.strip().lower()] = value.strip()
    
    # Fix server field (remove "tcp:" and ensure correct format)
    server_value = params.get('server', '').replace('tcp:', '')
    
    return {
        'ENGINE': 'mssql',
        'NAME': params.get('database', ''),
        'USER': params.get('uid', ''),  # Ensure UID is correctly extracted
        'PASSWORD': params.get('pwd', ''),  # Ensure PWD is correctly extracted
        'HOST': server_value.split(',')[0],  # Remove extra characters
        'PORT': '1433',
        'OPTIONS': {
            'driver': params.get('driver', 'ODBC Driver 17 for SQL Server'),
            'Encrypt': 'yes',
            'TrustServerCertificate': 'no',
        },
    }

# Apply the parsed connection string
if connection_string:
    DATABASES = {
        'default': parse_connection_string(connection_string)
    }
else:
    # Fallback database configuration (could be SQLite for local development)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# Security settings - Use environment variables to control these in different environments
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'False').lower() == 'true'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Security settings for production
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME type sniffing
SECURE_BROWSER_XSS_FILTER = True  # Enable XSS filtering in browsers
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True