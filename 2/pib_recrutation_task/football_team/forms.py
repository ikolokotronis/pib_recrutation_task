from django.core.exceptions import ValidationError
from django.forms.models import ModelForm

from .models import FootballPlayer


class FootballPlayerForm(ModelForm):
    class Meta:
        model = FootballPlayer
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        self.check_birth_year()
        self.check_team_nationality_limit()
        return cleaned_data

    def check_birth_year(self):
        birth_year = self.cleaned_data.get('birth_year')
        print(birth_year)
        if birth_year < 2000 and birth_year is not None:
            raise ValidationError("Niestety nie możesz dodać piłkarza, który urodził się przed 2000 rokiem.")
        return birth_year

    def check_team_nationality_limit(self):
        nationality = self.cleaned_data.get('nationality')
        club = self.cleaned_data.get('club')
        if nationality == 'non EU' and club is not None:
            non_eu_players_count = FootballPlayer.objects.filter(nationality='non EU', club=club).count()
            if non_eu_players_count >= 3:
                raise ValidationError("Nie można dodać 4 zawodnika spoza Unii Europejskiej.")
        return nationality
