from rest_framework import permissions


class IsWardenReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_warden)


class IsWarden(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_warden)

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_student)