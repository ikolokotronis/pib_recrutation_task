from django.db.models import Count, Q
from django.shortcuts import redirect
from django.views.generic.edit import CreateView

from .forms import FootballPlayerForm
from .models import FootballClub


class AddFootballPlayerView(CreateView):
    form_class = FootballPlayerForm
    template_name = "football_team/add_football_player.html"

    def form_valid(self, form):
        player = form.save()
        club = player.club
        self.__increment_no_players(club)

        player_name = f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}"
        subject = "Pomyślnie dodano piłkarza"
        message = f"Dodano poprawnie piłkarza  {player_name}"
        self.__send_mail(subject, message)

        return redirect("add_player")

    def __increment_no_players(self, club):
        club.no_players += 1
        club.save()
        return club

    def form_invalid(self, form):
        player_name = f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}"
        subject = f"Dodanie piłkarza nie powiodło się"
        message = f"Nie udało się dodać piłkarza {player_name}"
        self.__send_mail(subject, message)

        return super().form_invalid(form)

    def __send_mail(self, subject, msg):
        from_email = "nadawca@email.com"
        recipient_list = ["odbiorca@email.com"]
        # send_mail(subject, msg, from_email, recipient_list)
        return
