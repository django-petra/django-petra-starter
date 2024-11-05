from rest_framework.permissions import BasePermission

from modules.common.permissions.auth import IsAuthenticated

class Permissions(BasePermission):
  def get_permissions(self, view):
    if view.action == 'get_users':
      return [
        IsAuthenticated(),
      ]
    else:
      return []