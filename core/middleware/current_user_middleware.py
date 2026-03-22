from core.utils.current_user import set_current_user


class CurrentUserMiddleware:
    """
    Stores the current authenticated request user in thread-local storage
    so that BaseModel.save() can auto-populate created_by / updated_by.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_current_user(getattr(request, 'user', None))
        response = self.get_response(request)
        set_current_user(None)
        return response
