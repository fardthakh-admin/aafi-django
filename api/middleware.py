from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse

class AdminOnlyMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path.startswith('/api/'):
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('login'))
            elif not request.user.is_staff:
                return HttpResponseForbidden("You do not have permission to access this page.")
        return None