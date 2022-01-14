from django.http import HttpResponseRedirect
from django.contrib.auth import logout

def is_allowed_user(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if not request.user.is_anonymous and not (request.user.username == 'sebastienbarbier' or request.user.is_staff):
            logout(request)
            response = HttpResponseRedirect('/restricted/')
        else:
            response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware