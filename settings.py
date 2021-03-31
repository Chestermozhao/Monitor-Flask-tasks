# -*- coding: utf-8 -*-
import os

CELERY_BROKER_URL='redis://localhost:6379/0'
CELERY_RESULT_BACKEND='redis://localhost:6379/0'

# flask mail config
# set low security for your sender mail account
# https://myaccount.google.com/lesssecureapps
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = "<your-username>"
MAIL_PASSWORD = os.getenv('email_pwd')
MAIL_DEFAULT_SENDER = "<your-email-account>"
