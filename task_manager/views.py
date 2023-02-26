from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):

    template_name = "index.html"


class UserLoginView(SuccessMessageMixin, LoginView):

    template_name = 'login.html'
    next_page = 'home'
    success_message = _('You are logged in')


class UserLogoutView(SuccessMessageMixin, LogoutView):

    next_page = 'home'

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)
