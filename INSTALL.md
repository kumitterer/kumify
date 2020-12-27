# How to install Kumify on your machine

## Prerequisites

This project was tested with Python 3.8.6 on an Ubuntu Linux host. It should theoretically work on any system capable of running a current Python3 installation.

## Getting started

### Install required Python packages

(NB: You may want to do this in a venv – the details on how and why to do this are beyond the scope of this document.)

```pip3 install -r requirements.txt```

### Basic configuration

Any configuration you have to do takes place in a localsettings.py file in the project's root directory. Copy the provided localsettings.dist.py to localsettings.py and make any modifications you may need. The options are documented within that file.

### Creating superuser account

To create an account to login to your Kumify instance, you need to use the following command in the project's root directory:

```python3 manage.py createsuperuser```

You will be asked to provide a user name, email address and password.

### Run server

For your personal purposes, if you are running the application on your personal computer and don't need it to be available from the Internet, you may run the following command:

```python3 manage.py runserver```

The application is then available at [http://localhost:8000/].

If you want to make your Kumify instance available through a network, you will need to set up something like gunicorn and nginx. How this works is beyond the scope of this document. To prepare your static files for this, make sure ```STATIC_ROOT``` is set to the correct location in localsettings.py if you don't use S3, then run:

```python3 manage.py collectstatic```