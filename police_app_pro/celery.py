import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'police_app_pro.settings')
app = Celery('police_app_pro')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()