from django import forms
from economia.models import Player

class PlayerForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Player
        fields = ['id', 'email', 'password', 'player_name', 'school', 'nickname']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")

        return cleaned_data
