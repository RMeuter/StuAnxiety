from django.apps import AppConfig


class ModuleConfig(AppConfig):
    name = 'module'
    
    def ready(self):
        import module.signals.signal_module
        import module.signals.signal_sequence