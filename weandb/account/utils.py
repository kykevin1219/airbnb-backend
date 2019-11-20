import jwt

from weandb.settings    import SECRET_KEY
from django.http        import HttpResponse
from .models            import Users

def login_required(func) :
    def wrapper(self, request, *args, **kwargs) :
        access_token = request.headers.get('Authorization', None)
        if access_token is not None :
            try :
                payload = jwt.decode(access_token, SECRET_KEY, 'HS256')
                user_id = payload['user_id']
                user    = Users.objects.get(id = user_id)
                request.user = user
                return func(self, request, *args, *kwargs)
            except jwt.InvalidTokenError :
                return HttpResponse(status=401)
        else :
            return HttpResponse(status=401)
    return wrapper
