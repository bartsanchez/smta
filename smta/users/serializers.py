from rest_framework import reverse
from rest_framework import serializers

from users import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    balance_url = serializers.SerializerMethodField(
        help_text='Link to user\'s balance.',
    )

    class Meta:
        model = models.User
        fields = ('url', 'username', 'balance_url')

    def get_balance_url(self, obj):
        url = reverse.reverse(
            'user-balance',
            request=self.context.get('request', None),
            kwargs={'pk': obj.pk}
        )
        return url
