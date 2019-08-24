from django.apps import AppConfig


class ModuleConfig(AppConfig):
    name = 'module'
    
    def ready(self):
        import module.signal
        
