from django.forms import ModelForm, ValidationError

from home_page.models import Message


class MsgForm(ModelForm):
    class Meta:
        model = Message
        fields = '__all__'  # fix ('text',), ('__all__',)
        exclude = ('id',)

    def clean_text(self):
        data = self.cleaned_data['text']
        if data != data.lower():
            raise ValidationError('Please use low case')
        return data
