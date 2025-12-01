from flask_caching import Cache
from celery import Celery

# we initialise Cache
cache = Cache()

#Celery Application
# broker and backend point to reddis 
def make_celery(app_name=__name__):
    celery = Celery(app_name, 
                    broker='redis://localhost:6379/0',
                    backend='redis://localhost:6379/0')
    return celery

celery_app = make_celery()
