from django.core.exceptions import PermissionDenied

def owner_required(view_func):
    def wrapped_view(request,*args,**kwargs):
        if request.user.is_authenticated and getattr(request.user,'role',None) == 'owner':
            return view_func(request,*args,**kwargs)
        raise PermissionDenied
    return wrapped_view