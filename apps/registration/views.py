from django.shortcuts import render
from .forms import RegistrationForm
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

# Create your views here.

"""
This module will define views for Registration app
"""

class HomeView(View):
    """
    This class will define the home view
    """
    template_name = "registration/home.html"

    def get(self, request, *args, **kwargs):
        """
        This method will render the home page
        Arguments:
            request {object} -- Request object
        Returns:
            object -- HttpResponse object
        """
        context = {}
        return render(request, self.template_name, context)

class UserRegistrationView(FormView):
    """
    This class will define the user registration view
    """
    template_name = "registration/user_registration.html"
    form_class = RegistrationForm
    success_url = reverse_lazy(viewname="registration:login")

    def form_valid(self, form):
        """
        This method will save the form and redirect to login page
        Arguments:
            form {object} -- Form object
        Returns:
            object -- HttpResponse object
        """
        form.save()
        return super().form_valid(form)