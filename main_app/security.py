from pyramid.authentication import AuthTktCookieHelper
from pyramid.authorization import ACLHelper, Authenticated, Everyone


# fonte: https://docs.pylonsproject.org/projects/pyramid/en/latest/whatsnew-2.0.html#upgrading-auth-20
class MySecurityPolicy:
    def __init__(self, secret):
        self.helper = AuthTktCookieHelper(secret)

    def identity(self, request):
        identity = self.helper.identify(request)
        if identity is None:
            return None
        userid = identity['userid']

        # assuming the userid is valid, return a map with userid and principals
        return {
            'userid': userid,

        }

    def authenticated_userid(self, request):
        # defer to the identity logic to determine if the user id logged in
        # and return None if they are not
        identity = request.identity
        if identity is not None:
            return identity['userid']

    def permits(self, request, context, permission):
        # use the identity to build a list of principals, and pass them
        # to the ACLHelper to determine allowed/denied
        identity = request.identity
        principals = set([Everyone])
        if identity is not None:
            principals.add(Authenticated)
            principals.add(identity['userid'])
        return ACLHelper().permits(context, principals, permission)

    def remember(self, request, userid, **kw):
        return self.helper.remember(request, userid, **kw)

    def forget(self, request, **kw):
        return self.helper.forget(request, **kw)
