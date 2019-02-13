from django.apps import AppConfig


class MusicsConfig(AppConfig):
    name = 'musics'

    def ready(self):
        import musics.signals