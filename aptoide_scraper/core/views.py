from typing import Dict
from django.http.response import Http404
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from django.http import HttpResponse
from django.urls.base import reverse_lazy
from django.views import generic
from requests.models import HTTPError
from urllib.error import URLError
from .models import AptoideApp
from .forms import UrlForm


class IndexView(generic.FormView):
    """Home view for the aptoide app scrapping service.

    It shows a form of one url input field with a button to scrap the targetted url. Allowed methods are get and post, get redirects to the index url with an empty form to fill and validate, post does the same with pre-filled form, validation check and, if valid, redirection to the success url.

    Attributes
    ----------
    template_name : str
        Path to the html template to use for the view (relatively to ./templates/).
    form_class : Type[Form]
        Form class to use.
    """

    template_name = "core/index.html"
    form_class = UrlForm

    def form_valid(self, form: UrlForm) -> HttpResponse:
        """Happens whenever the form is considered valid.

        Calls the scrap_url method and update/create an AptoideApp instance from returned data. Then it sets the success_url to redirect to the detail view of the created/updated instance.

        Parameters
        ----------
        form : UrlForm
            Form instance which has been validated.

        Returns
        -------
        HttpResponse
            The http response to return.
        """
        id = urlparse(form.data["url"]).netloc.split(".")[0]
        try:
            scraped_data = self.scrap_url(form.data["url"])
        except (AttributeError, HTTPError, URLError):
            raise Http404
        AptoideApp.objects.update_or_create(scraped_data, pk=id)
        self.success_url = reverse_lazy(
            "core:detail",
            kwargs={"pk": id},
        )
        return super().form_valid(form)

    def scrap_url(self, url: str) -> Dict[str, str]:
        """Scraps the targetted url with beautiful soup.

        Request the url to scraps and gathers data into an AptoideApp model's instance.

        Parameters
        ----------
        url : str
            The url to scrap.

        Returns
        -------
        Dict[str, str]
            The aptoide application scraped data.
        """
        request = requests.get(url)
        soup = BeautifulSoup(request.content, "html5lib")
        try:
            downloads_number = soup.find(
                "span", attrs={"class": "mini-stats__Info-sc-188veh1-6 hwoUxO"}
            ).text
        except AttributeError:
            downloads_number = soup.find(
                "span", attrs={"class": "mini-stats__Info-sc-188veh1-6 goCMQs"}
            ).text
        return {
            "name": soup.find("meta", attrs={"itemprop": "name"}).get("content"),
            "version": soup.find("meta", attrs={"itemprop": "version"}).get("content"),
            "release_date": soup.find("meta", attrs={"itemprop": "datePublished"}).get(
                "content"
            ),
            "downloads_number": downloads_number,
            "description": soup.find("p", attrs={"itemprop": "description"}).text,
        }


class DetailView(generic.DetailView):
    """Detail view of an aptoide app.

    A direct get request to the url will lead to a 404 error if the app has never been scraped. This view automatically rejecst other http methods than get (the only implemented).

    Attributes
    ----------
    model : AptoideApp
        The django model to base the detail view on.
    template_name : str
        Path to the html template to use for the view (relatively to ./templates/).
    context_object_name : str
        Name of the AptoideApp instance in context (in template a fortiori).
    """

    model = AptoideApp
    template_name = "core/detail.html"
    context_object_name = "aptoide_app"
