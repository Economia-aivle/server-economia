from django import forms
from economia.models import Scenario

class ScenarioForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = ['title', 'subjects', 'question_text']