from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuration class of the core scraping application.

    Attributes
    ----------
    default_auto_field : str
        Default automatic field class used for application's model.
    name : str
        Application's name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
