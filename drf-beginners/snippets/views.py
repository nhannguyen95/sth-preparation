from django.contrib.auth.models import User

from rest_framework import generics, permissions, renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Snippet
from .permissions import IsOwnerOrReadOnly
from .serializers import SnippetSerializer, UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
  return Response({
    'users': reverse('user-list', request=request, format=format),
    'snippets': reverse('snippet-list', request=request, format=format)
  })


class SnippetList(generics.ListCreateAPIView):
  """Provide a get method handle for querying a collection of model instances."""
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
  """Provide a get method handle for querying a single model instance."""
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


class SnippetHighlight(generics.GenericAPIView):
  queryset = Snippet.objects.all()
  renderer_classes = (renderers.StaticHTMLRenderer,)

  def get(self, request, *args, **kwargs):
    snippet = self.get_object()
    return Response(snippet.highlighted)


class UserList(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
