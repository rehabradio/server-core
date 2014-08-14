from django.conf import settings
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).
    """
    def process_request(self, request):
        whilte_list = [
            settings.LOGIN_URL,
            '/complete/google-oauth2/',
            '/api/_auth/login/'
        ]
        if not request.user.is_authenticated():
            if request.path_info not in whilte_list:
                return redirect('/login/google-oauth2/?next=/test/')
