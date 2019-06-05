from django.apps import AppConfig


class CarbonConfig(AppConfig):
    name = 'carbon'

    
    def ready(self):
        from .updater import start
        start()