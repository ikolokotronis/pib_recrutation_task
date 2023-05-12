from django.forms.models import ModelForm

from .models import FootballPlayer


class FootballPlayerForm(ModelForm):
    class Meta:
        model = FootballPlayer
        fields = '__all__'
