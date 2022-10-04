from django.shortcuts import render
from .forms import RegistrationForm
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

# Create your views here.

class UserRegistrationView(FormView):
    template_name = "registration/user_registration.html"
    form_class = RegistrationForm
    success_url = reverse_lazy(viewname="registration:login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)