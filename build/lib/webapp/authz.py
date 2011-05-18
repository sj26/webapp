from webapp.check import Check, environ_has

def has_permission(perm):
    return Check(lambda app: app.__authorized_to__(perm))

def has_any_permission(*perms):
    return Check(lambda app: any(app.__authorized_to__(perm) for perm in perms))

def has_all_permissions(*perms):
    return Check(lambda app: all(app.__authorized_to__(perm) for perm in perms))

class Authorizing(object):
    def __authorized_to__(self, permission):
        raise NotImplemented()

