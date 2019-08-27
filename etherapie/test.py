from django.test import TestCase, Client
from django.urls import resolve, reverse
from .urls import urlpatterns

class TestUrls (TestCase):

    def setUp(self):
        self.client =Client()
        self.home_url=reverse("home")
        self.FAQ_url=reverse("FAQ")
        self.contact_url=reverse("contact")


    def test_home_GET(self):
        reponse = self.client.get(self.home_url)

        self.assertEquals(reponse.status_code, 200)
        self.assertTemplateUsed(reponse, "home.html")

    def test_FAQ_GET(self):
        reponse = self.client.get(self.FAQ_url)

        self.assertEquals(reponse.status_code, 200)
        self.assertTemplateUsed(reponse, "FAQ.html")

    def test_contact_GET(self):
        reponse = self.client.get(self.contact_url)

        self.assertEquals(reponse.status_code, 200)
        self.assertTemplateUsed(reponse, "contact.html")