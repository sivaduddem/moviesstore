#apps.py
from django.apps import AppConfig  # Import Django's application configuration base class


class PetitionsConfig(AppConfig):  # Define the app configuration for the petitions app
    default_auto_field = 'django.db.models.BigAutoField'  # Use BigAutoField for primary keys by default
    name = 'petitions'  # The Python path to this app
