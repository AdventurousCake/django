from rest_framework import serializers

from home_page.models import Message


class MsgSerializer(serializers.ModelSerializer):
    # author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'text', 'created_date')
        # read_only_fields = ('post', 'created')
        model = Message


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post', 'created')
        # model = Comment