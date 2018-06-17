from rest_framework import viewsets

from transfers import models
from transfers import serializers


class TransferViewSet(viewsets.ModelViewSet):
    queryset = models.Transfer.objects.all()
    serializer_class = serializers.TransferSerializer
