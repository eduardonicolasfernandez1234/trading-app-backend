from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'deleted_at', 'is_active', 'is_deleted'
        ]
