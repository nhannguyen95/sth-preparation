from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
  """
  Custom permission to only allow owners of an object to edit it.
  """
  def has_object_permission(self, request, view, obj):
    # We will always allow GET, HEAD and OPTIONS requests.
    if request.method in permissions.SAFE_METHODS:
      return True

    # Write permissions are only allowed to the owner of the snippet.
    return obj.owner == request.user
