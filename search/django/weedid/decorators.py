from django.http import HttpResponseForbidden, HttpResponseNotAllowed


def decorator_post_logged_in(view_func):
    def _wrapped_view(cls, request, *args, **kwargs):
        if not request.method == "POST":
            return HttpResponseNotAllowed(request.method)
        if not (request.user and request.user.is_authenticated):
            return HttpResponseForbidden("You dont have access to proceed")
        return view_func(cls, request, *args, **kwargs)

    return _wrapped_view
