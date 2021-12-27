import secrets

from rest_framework.permissions import BasePermission
from django.core.cache import cache

class PostTokenValidation(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ("DELETE", "PUT", "PATCH"):
            if "Authorization" in request.headers:
                head = request.headers["Authorization"].split(" ")
                if "Token" == head[0]:
                    token = head[1]
                    return secrets.compare_digest(token, obj.password)
        else: # "POST" and "GET" are allowed
            return True
        return False
