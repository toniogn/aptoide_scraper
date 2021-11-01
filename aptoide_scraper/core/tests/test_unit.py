from urllib.parse import urlparse
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse


class TestIndexView(TestCase):
    """Here lies the tests for allowed http methods on the index view."""

    def setUp(self) -> None:
        self.client = Client()
        self.valid_available_url = "https://lords-mobile.en.aptoide.com/app"
        self.valid_unavailable_url = "https://unavailable-url.en.aptoide.com/app"
        self.invalid_url = "https://invalid-url.dummy.com"

    def test_get_integrity(self):
        """Tests the GET request response at index view url."""
        response = self.client.get(reverse("core:index"))
        self.assertEqual(response.status_code, 200)

    def test_post_valid_form_available_url_integrity(self):
        """Tests the POST request response at index view url with a valid available url.

        The request should leed to redirection to the detail view corresponding to the scraped app.
        """
        response = self.client.post(
            reverse("core:index"), data={"url": self.valid_available_url}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/" + urlparse(self.valid_available_url).netloc.split(".")[0] + "/",
        )

    def test_post_invalid_form_integrity(self):
        """Tests the POST request response at index view url with an invalid url.

        The request should leed to the index view with an invalid form message.
        """
        response = self.client.post(
            reverse("core:index"), data={"url": self.invalid_url}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid URL.")

    def test_post_valid_form_unavailable_url_integrity(self):
        """Tests the POST request response at index view url with a valid unavailable url.

        The request should leed to a 404 error because of the unavailability of the url (URLError).
        """
        response = self.client.post(
            reverse("core:index"), data={"url": self.valid_unavailable_url}
        )
        self.assertEqual(response.status_code, 404)
