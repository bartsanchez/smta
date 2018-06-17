from rest_framework import reverse
from rest_framework import serializers

from transfers import models


class TransferSerializer(serializers.HyperlinkedModelSerializer):
    execute_url = serializers.SerializerMethodField(
        help_text='Link to transfer execution.',
    )

    class Meta:
        model = models.Transfer
        fields = (
            'url', 'from_user', 'to_user', 'quantity', 'state', 'execute_url',
        )

    def get_execute_url(self, obj):
        url = reverse.reverse(
            'transfer-execute',
            request=self.context.get('request', None),
            kwargs={'pk': obj.pk}
        )
        return url
