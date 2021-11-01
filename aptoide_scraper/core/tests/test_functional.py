from urllib.parse import urlparse
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from core.forms import UrlForm
from itertools import cycle


class TestFunctional(TestCase):
    """Here lies some functional tests of the web service."""

    def setUp(self) -> None:
        self.client = Client()
        self.urls = (
            url.format(langage_tag)
            for langage_tag, url in zip(
                UrlForm.LANGAGES_TAGS,
                cycle(
                    (
                        "https://lords-mobile.{}.aptoide.com/app",
                        "https://clean-master.{}.aptoide.com/app",
                        "https://nba-now-22.{}.aptoide.com/app",
                        "https://my-talking-tom.{}.aptoide.com/app",
                    )
                ),
            )
        )

    def test_multilangage_functional_integrity(self):
        """Test each functional aptoide app url for each langage tag.
        
        Expects a redirection to the detail view of the AptoideApp model's instance.
        """
        for url in self.urls:
            with self.subTest(url=url):
                response = self.client.post(reverse("core:index"), data={"url": url})
                self.assertEqual(response.status_code, 302)
                self.assertEqual(
                    response.url,
                    "/" + urlparse(url).netloc.split(".")[0] + "/",
                )
