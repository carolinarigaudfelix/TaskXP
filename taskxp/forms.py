from django import forms

from .models import Tarefaxp

class TarefaForm(forms.ModelForm):

    class Meta:
        model = Tarefaxp
        fields =('title','description')