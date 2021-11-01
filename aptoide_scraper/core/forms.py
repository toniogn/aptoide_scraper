from django import forms
from django.core.validators import URLValidator


class UrlForm(forms.Form):
    """Form subclass integrating a url input character field.

    Attributes
    ----------
    url : URLField
        An url character field with a specific regex to insure the url to be an aptoide application in any allowed langages (see LANGAGES_TAGS attribute).
    """

    LANGAGES_TAGS = (
        "en",
        "pt",
        "br",
        "fr",
        "es",
        "mx",
        "de",
        "it",
        "ru",
        "sa",
        "id",
        "in",
        "bd",
        "mr",
        "pa",
        "my",
        "th",
        "vn",
        "tr",
        "cn",
        "ro",
        "mm",
        "pl",
        "rs",
        "hu",
        "gr",
        "bg",
        "nl",
        "ir",
        "jp",
        "ua",
        "kr",
    )
    url = forms.URLField(
        validators=[
            URLValidator(
                regex="https:\/\/([a-zA-Z0-9]*-?)*\.("
                + "|".join(LANGAGES_TAGS)
                + ")\.aptoide\.com\/app"
            )
        ]
    )
