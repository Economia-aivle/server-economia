from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    player_id = serializers.CharField(max_length=20)
    pwd = serializers.CharField(max_length=255)