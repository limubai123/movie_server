from django.contrib.auth.models import User
from rest_framework import generics, permissions

from .serializers import RegisterSerializer


class RegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    serializer_class = RegisterSerializer
