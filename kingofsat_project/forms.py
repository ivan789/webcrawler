from models import  Kanali
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Kanali
        fields = ('channel',)


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file')