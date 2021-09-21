from rest_framework import serializers

from .models import Block, Transaction


class BlockModelSerializer(serializers.ModelSerializer):
    blockNumber = serializers.ReadOnlyField()
    timeStamp = serializers.ReadOnlyField()
    blockMiner = serializers.ReadOnlyField()
    blockReward = serializers.ReadOnlyField()
    uncles = serializers.ReadOnlyField()
    uncleInclusionReward = serializers.ReadOnlyField()

    class Meta:
        model = Block
        fields = "__all__"

    def to_representation(self, instance):
        representation = instance.data
        return super().to_representation(representation)


class TransactionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def to_representation(self, instance):
        representation = instance.data
        return super().to_representation(representation)
