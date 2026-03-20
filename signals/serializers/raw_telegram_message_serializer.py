from core.serializers.base_model_serializer import BaseModelSerializer
from signals.models import RawTelegramMessage


class RawTelegramMessageSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = RawTelegramMessage
        fields = '__all__'
