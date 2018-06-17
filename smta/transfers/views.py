from django import shortcuts

from rest_framework import decorators
from rest_framework import response
from rest_framework import status
from rest_framework import viewsets

from transfers import models
from transfers import serializers


class TransferViewSet(viewsets.ModelViewSet):
    queryset = models.Transfer.objects.all()
    serializer_class = serializers.TransferSerializer

    @decorators.action(methods=['post'], detail=True)
    def execute(self, request, pk):
        transfer = shortcuts.get_object_or_404(models.Transfer, pk=pk)

        if transfer.state != 'PENDING':
            return response.Response(
                {'detail': 'The order is not ready to be sent.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Only admins and logged user itself should be able to make transfers
        if (
            (not request.user.is_superuser) and
            (request.user.pk != transfer.from_user.pk)
        ):
            return response.Response(
                {
                    'detail':
                    'You don\'t have permissions to execute this transfer'
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        transfer.execute_transfer()

        return response.Response({'detail': 'Success'})
