from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

class AdminOnlyMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path.startswith('/api/') and not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to access this page.")
        return None
