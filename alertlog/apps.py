from django.apps import AppConfig


class AlertlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alertlog'
    
    
    def ready(self):
        print("Starting Sheduler")
        
        # getdatafrom_mysql.start()
