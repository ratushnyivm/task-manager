from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    """Generic class-based view for a home page."""

    template_name = "index.html"


class UserLoginView(SuccessMessageMixin, LoginView):
    """Generic class-based view for user login."""

    template_name = 'login.html'
    next_page = 'home'
    success_message = _('You are logged in')


class UserLogoutView(SuccessMessageMixin, LogoutView):
    """Generic class-based view for user logout."""

    next_page = 'home'

    def dispatch(self, request, *args, **kwargs):
        messages.info(self.request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)


def error(request):
    a = None
    a.hello()
    return HttpResponse('You shouldn\'t be seeing this')
