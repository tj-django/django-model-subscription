from django.apps import AppConfig


class DemoConfig(AppConfig):
    name = 'demo'

    def ready(self):
        from demo import subscription  # noqa: F401
