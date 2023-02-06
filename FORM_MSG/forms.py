from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ValidationError
from core.models import User
from .models import Message, Comment


class MsgForm(ModelForm):
    class Meta:
        model = Message
        fields = '__all__'  # fix ('text',), ('__all__',)
        exclude = ('id', 'author')
        help_texts = {'text': "Validator check this", 'name': 'Your name'}

    # clean_FIELD validation
    def clean_text(self):
        data = self.cleaned_data['text']
        if data != data.lower():
            raise ValidationError('Please use low case')
        return data

    def clean_accept_terms(self):
        data = self.cleaned_data['accept_terms']
        if not data:
            raise ValidationError('You should accept terms')
        return data


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


# форма регистрации
class CreationFormUser(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # порядок полей
        fields = ("first_name", "last_name", "username", "email")
