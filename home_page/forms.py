from django.forms import ModelForm

from home_page.models import Message


class MsgForm(ModelForm):
    class Meta:
        model = Message
        fields = '__all__'  # fix ('text',), ('__all__',)
