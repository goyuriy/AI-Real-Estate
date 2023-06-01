from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task'

class AssignedTaskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assigned_task'
