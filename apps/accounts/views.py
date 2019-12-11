from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, UpdateView

from oidc_provider.models import UserConsent

from apps.accounts.forms import UserForm


class UserView(LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('account_profile')


class ConsentList(LoginRequiredMixin, ListView):
    template_name = 'consent_list.html'
    model = UserConsent

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


__all__ = ['UserView', 'ConsentList']
