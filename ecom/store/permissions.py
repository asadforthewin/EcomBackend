from rest_framework.permissions import BasePermission, DjangoModelPermissions
from rest_framework import permissions

class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
    

# class FullDjangoPermissions(DjangoModelPermissions):
#     def __init__(self) -> None:
#         self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class ViewCustomerHistory(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('store.view_history') #The user has method has_perm where we pass the
    #app name along with the code name of the permission