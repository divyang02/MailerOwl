from http import HTTPStatus
from django.test import TestCase
from ..forms import RegistrationForm


class TestViews(TestCase):
    def test_user_registration_view_get(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_registration_view_post(self):
        data = {
            "username": "test123",
            "email": "test123@gmail.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
        response = self.client.post("/register/", data=data)
        self.assertRedirects(
            response,
            "/login/",
            status_code=302,
            target_status_code=200,
        )
