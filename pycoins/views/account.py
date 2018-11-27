from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils.http import urlencode
from rest_auth.registration.views import VerifyEmailView


class EmailConfirmationView(VerifyEmailView):
    allowed_methods = ('GET', 'POST', 'OPTIONS', 'HEAD')

    def get(self, request, *args, **kwargs):
        request.data['key'] = self.kwargs['key']
        response = super(EmailConfirmationView, self).post(request, *args, **kwargs)

        query = {}
        if response.status_code == 200:
            query['info'] = "Your email has been confirmed."
        else:
            query['info'] = response.content['detail']

        return HttpResponseRedirect("{}?{}".format(reverse('login'), urlencode(query)))


confirm_email = EmailConfirmationView.as_view()
