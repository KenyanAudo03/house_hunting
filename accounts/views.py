from django.shortcuts import render
from allauth.account.views import ConfirmEmailView
from django.contrib.auth import login
from django.shortcuts import redirect

class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        if self.object and self.object.email_address:
            user = self.object.email_address.user
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            list(self.request._messages)[:] = []  # Clear existing messages
        return redirect('/')
