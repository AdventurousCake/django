from rest_framework import serializers
from core.models import User
from home_page.models import Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # нельзя вместе fields и exclude, и без них по отдельности
        # не юзать лишние поля, которые связаны с правами и группами
        # fields = '__all__'
        fields = ('id', 'username')
        # exclude = ('password',)
        model = User


class MsgSerializerSearch(serializers.ModelSerializer):
    # author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('text',)
        model = Message


class MsgSerializer(serializers.ModelSerializer):
    # author = serializers.StringRelatedField(read_only=True)

    author = UserSerializer(read_only=True)  # not many!
    # or save in perform create

    class Meta:
        fields = ('id', 'name', 'text', 'created_date', 'author') # 'author'
        read_only_fields = ('author',)
        # read_only_fields = ('post', 'created', 'OWNER')
        model = Message

    def validate_text(self, value):
        if value == 'not valid':
            raise serializers.ValidationError('Проверьте text (validate_text validator)')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post', 'created')
        # model = Comment
