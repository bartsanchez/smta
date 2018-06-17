from rest_framework import serializers

from transfers import models


class TransferSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Transfer
        fields = ('url', 'from_user', 'to_user', 'quantity')
