from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
    
    def ready(self):
        # L'initialisation de l'admin est maintenant gérée par admin.py
        pass



    
    