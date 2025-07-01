from django import forms
from apps.auxiliares.models.responsable import Responsable

class ResponsableForm(forms.ModelForm):
    class Meta:
        model = Responsable
        fields = '__all__'
        widgets = {
            'nombres_apellidos': forms.TextInput(attrs={'readonly': 'readonly'}),
            'cargo': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
