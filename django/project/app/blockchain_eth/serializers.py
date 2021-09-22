from datetime import datetime

from rest_framework import serializers

from .models import Block, Transaction


class BlockModelSerializer(serializers.ModelSerializer):
    blockNumber = serializers.ReadOnlyField()
    timeStamp = serializers.ReadOnlyField()
    timeStampDateTime = serializers.SerializerMethodField()
    blockMiner = serializers.ReadOnlyField()
    blockReward = serializers.ReadOnlyField()
    uncles = serializers.ReadOnlyField()
    uncleInclusionReward = serializers.ReadOnlyField()

    class Meta:
        model = Block
        exclude = ["number"]

    def to_representation(self, instance):
        representation = instance.data
        return super().to_representation(representation)

    def get_timeStampDateTime(self, obj):
        date_time = datetime.utcfromtimestamp(int(obj["timeStamp"]))
        return date_time


class TransactionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def to_representation(self, instance):
        representation = instance.data
        return super().to_representation(representation)
