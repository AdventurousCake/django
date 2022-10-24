from rest_framework import serializers
from core.models import User
from home_page.models import Message

class MsgSerializerSIMPLE(serializers.ModelSerializer):
    # author = serializers.StringRelatedField(read_only=True)
    class Meta:
        fields = ('text',)
        model = Message

class UserSerializer(serializers.ModelSerializer):
    # messages = serializers.StringRelatedField(read_only=True, many=True)
    messages = MsgSerializerSIMPLE(many=True) # MANY TRUE
    class Meta:
        # нельзя вместе fields и exclude, и без них по отдельности
        # не юзать лишние поля, которые связаны с правами и группами

        # fields = '__all__'
        fields = ('id', 'username', 'messages')
        # exclude = ('password',)

        model = User


class MsgSerializer(serializers.ModelSerializer):
    # author = serializers.StringRelatedField(read_only=True)

    author = UserSerializer(read_only=True)  # not many!

    # or save in perform create

    class Meta:
        fields = ('id', 'name', 'text', 'created_date', 'author', 'msg_length')  # 'author'
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
