from django import shortcuts

from rest_framework import decorators
from rest_framework import response
from rest_framework import status
from rest_framework import viewsets

from users import models
from users import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    @decorators.action(detail=True)
    def balance(self, request, pk):
        user = shortcuts.get_object_or_404(models.User, pk=pk)

        # Only admins and logged user itself should be able to view a balance
        if not request.user.is_superuser and request.user.pk != user.pk:
            return response.Response(
                {'detail': 'You don\'t have permissions to view this balance'},
                status=status.HTTP_403_FORBIDDEN,
            )

        return response.Response({'balance': user.get_balance()})
