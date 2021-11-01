from django.db import models


class AptoideApp(models.Model):
    """Aptoide application model.
    
    The aptoide application model to store in database and display in associated detail view.

    Attributes
    ----------
    id : CharField
        The primary key of the application, part of it's parsed url netloc attribute (see IndexView).
    name : CharField
        The name of the application.
    version : CharField
        The version of the application.
    downloads_number : CharField
        The downloads number of the application (in millions (M) or thousands (K)).
    release_date : DateField
        The release date of the application's current version.
    description : 
        The description of the application.
    """
    id = models.CharField(max_length=150, primary_key=True, unique=True)
    name = models.CharField(max_length=150)
    version = models.CharField(max_length=150)
    downloads_number = models.CharField(max_length=150)
    release_date = models.DateField()
    description = models.CharField(max_length=500)

    class Meta:
        verbose_name = "aptoide app"
