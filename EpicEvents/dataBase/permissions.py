from rest_framework.permissions import BasePermission

owner_methods = ('PUT', 'DELETE')


class HasCustomerPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in owner_methods:
            if request.user.role == 'Sales':
                return True


class HasContractPermission(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in owner_methods:
            if request.user.role == 'Sales':
                return True


class HasEventPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in owner_methods:
            if obj.support == request.user or obj.contract.sales == request.user:
                return True
