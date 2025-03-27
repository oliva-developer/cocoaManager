from django.apps import AppConfig


class ApisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apis_'
    verbose_name = "OliSYS"

    def ready(self):
        from apis_.dash_apps import declare_dash_app
        declare_dash_app()