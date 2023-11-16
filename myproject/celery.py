import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTING_MODULE','myproject.settings')

app = Celery('myproject')

app.config_from_object('django.conf:settings',namespace='CELERY')


app.conf.beat_schedule ={
    'get_koke_3s':{
        'task':'alertlog.tasks.get_joke',
        'schedule': 70.0 # every 5 seconds
    },
     'func2-every-3-minutes': {

        'task': 'alertlog.tasks.countdata',
        'schedule': 10.0,

    },
    
}

app.autodiscover_tasks()

