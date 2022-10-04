from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        """
        While saving the user we need to make sure that the registered user should have viewing access
        of our models and it should be a staff user so that it can access admin page.
        """
        user = super(RegistrationForm, self).save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
            app_models = apps.get_app_config("email_scheduler").get_models()
            for model in app_models:
                permission_codename = "view_" + model._meta.model_name
                content_type = ContentType.objects.get_for_model(model)
                permission = Permission.objects.get(
                    codename=permission_codename, content_type=content_type
                )
                user.user_permissions.add(permission)
        return user
