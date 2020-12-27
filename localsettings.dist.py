# The secret key must be a long random string. 
# You may use the django.core.management.utils.get_random_secret_key() function to generate one, or just smash your keyboard real hard a few times.

SECRET_KEY = "longrandomstring"

# Putting the system in debug mode will give you a lot of output if an error occurs, but it potentially exposes sensitive information like passwords.
# Only set this to True if you really need to, especially if you are running a public instance.

DEBUG = False

# You may set this variable to a list of domain names that are allowed to be used to access your instance.

ALLOWED_HOSTS = ["*"] # Rationale: The application should be running behind a reverse proxy anyway if it's public - let that handle which hosts are allowed

# If you are using an external server to make your instance public, we need to store some static files somewhere.
# Enter the appropriate directory and make sure your webserver serves that location at /static/

STATIC_ROOT = '/var/www/html/static/'

# By default, all files, including uploads, are stored locally. 
# You may use an S3 compatible storage instead in order to increase reliability and decrease disk usage.
# If AWS_ACCESS_KEY_ID is set to None, local storage will be used.
# See https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html for all options you can use here.
# (NB: Only options starting with "AWS_" are allowed here, the storage configuration will be handled automatically.)

AWS_ACCESS_KEY_ID = None
AWS_SECRET_ACCESS_KEY = None
AWS_STORAGE_BUCKET_NAME = None
AWS_S3_ENDPOINT_URL = None

# By default, this application uses a local sqlite3 database file. You can choose to use a MariaDB/MySQL database instead.
# If DB_HOST is set to None, the sqlite3 database will be used.

DB_HOST = None # Host name of the database server
DB_PORT = 3306 # Port of the database server - the default value usually works
DB_NAME = None # Name of the database to be used
DB_USER = None # User name to authenticate with
DB_PASS = None # Password to authenticate with