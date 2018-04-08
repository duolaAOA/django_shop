from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = "用户操作管理"

    def ready(self):
        import users.singals