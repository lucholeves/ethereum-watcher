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


class TransactionInternalModelSerializer(serializers.ModelSerializer):
    # NOTE: internal transactions aren't transactions per se
    to_id = serializers.ReadOnlyField(source="to")
    from_id = serializers.ReadOnlyField(source="from")
    gas = serializers.ReadOnlyField()
    hash = serializers.ReadOnlyField()
    type = serializers.ReadOnlyField()
    input = serializers.ReadOnlyField()
    value = serializers.ReadOnlyField()
    errCode = serializers.ReadOnlyField()
    gasUsed = serializers.ReadOnlyField()
    isError = serializers.ReadOnlyField()
    traceId = serializers.ReadOnlyField()
    timeStamp = serializers.ReadOnlyField()
    timeStampDateTime = serializers.SerializerMethodField()
    blockNumber = serializers.ReadOnlyField()
    contractAddress = serializers.ReadOnlyField()

    class Meta:
        model = Transaction
        exclude = ["block"]

    def to_representation(self, instance):
        representation = instance.data
        return super().to_representation(representation)

    def get_timeStampDateTime(self, obj):
        date_time = datetime.utcfromtimestamp(int(obj["timeStamp"]))
        return date_time


class TransactionNormalModelSerializer(serializers.ModelSerializer):
    to_id = serializers.ReadOnlyField(source="to")
    from_id = serializers.ReadOnlyField(source="from")
    r = serializers.ReadOnlyField()
    s = serializers.ReadOnlyField()
    v = serializers.ReadOnlyField()
    gas = serializers.ReadOnlyField()
    hash = serializers.ReadOnlyField()
    type = serializers.ReadOnlyField()
    input = serializers.ReadOnlyField()
    nonce = serializers.ReadOnlyField()
    value = serializers.ReadOnlyField()
    chainId = serializers.ReadOnlyField()
    gasPrice = serializers.ReadOnlyField()
    blockHash = serializers.ReadOnlyField()
    accessList = serializers.ReadOnlyField()
    blockNumber = serializers.ReadOnlyField()
    maxFeePerGas = serializers.ReadOnlyField()
    transactionIndex = serializers.ReadOnlyField()
    maxPriorityFeePerGas = serializers.ReadOnlyField()

    class Meta:
        model = Transaction
        exclude = ["block"]

    def to_representation(self, instance):
        representation = instance.data
        return super().to_representation(representation)
