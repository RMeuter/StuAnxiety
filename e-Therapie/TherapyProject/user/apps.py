from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'
    verbose_name = ('Utilisateur')
    
    def ready(self):
        import user.signal