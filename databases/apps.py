from django.apps import AppConfig


# class DatabasesConfig(AppConfig):
#     name = 'databases'

class DatabasesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'databases'
    label = 'databases_app'
