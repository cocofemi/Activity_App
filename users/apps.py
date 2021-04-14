from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
    	import users.signals # imports the signals for automatically creating and saving a new user profile. 