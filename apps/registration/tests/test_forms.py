from django.test import TestCase
from ..forms import RegistrationForm
from django.contrib.auth.models import User


class TestForm(TestCase):

    def test_form_error_when_password_mismatch(self):
        form = RegistrationForm(
            data={
                "username": "test123",
                "email": "test123@gmail.com",
                "password1": "Password@123",
                "password2": "NotPassword@123",
            })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password2"],
                         ["The two password fields didn’t match."])

    def test_form_valid(self):
        form = RegistrationForm(
            data={
                "username": "test123",
                "email": "test123@gmail.com",
                "password1": "Password@123",
                "password2": "Password@123",
            })
        self.assertTrue(form.is_valid())

    def test_all_permission(self):
        form = RegistrationForm(
            data={
                "username": "test123",
                "email": "test123@gmail.com",
                "password1": "Password@123",
                "password2": "Password@123",
            })
        self.assertTrue(form.is_valid())
        form.save()
        created_user_queryset = User.objects.filter(username="test123")
        self.assertTrue(created_user_queryset.exists())
        created_user = created_user_queryset[0]
        self.assertTrue(
            created_user.has_perm("email_scheduler.view_emailscheduler"))
        self.assertTrue(
            created_user.has_perm("email_scheduler.view_emailschedulerlogs"))
        self.assertTrue(created_user.is_staff)
