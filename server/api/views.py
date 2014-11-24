from django.contrib.auth import get_user_model

from rest_framework import authentication, permissions, viewsets

from api.mixins import DefaultsMixin
from api.serializers import UserSerializer

User = get_user_model()

class UserViewSet(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
    """API endpoint for listing users."""
    
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer