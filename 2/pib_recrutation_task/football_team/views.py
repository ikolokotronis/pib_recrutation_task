from django.db.models import Count, Q
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.contrib import messages

from .forms import FootballPlayerForm
from .models import FootballClub


class AddFootballPlayerView(CreateView):
    form_class = FootballPlayerForm
    template_name = "football_team/add_football_player.html"

    def form_valid(self, form):
        player = form.save()
        club = player.club
        self.__increment_no_players(club)
        self.__send_mail_success(form)
        messages.add_message(self.request, messages.INFO, "Dodano piłkarza")
        return redirect("add_player")

    def form_invalid(self, form):
        self.__send_mail_failure(form)

        return super().form_invalid(form)

    def __increment_no_players(self, club):
        club.no_players += 1
        club.save()
        return club

    def __send_mail_success(self, form):
        player_name = f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}"
        subject = "Pomyślnie dodano piłkarza"
        message = f"Dodano poprawnie piłkarza  {player_name}"
        self.__send_mail(subject, message)

    def __send_mail_failure(self, form):
        player_name = f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}"
        subject = f"Dodanie piłkarza nie powiodło się"
        message = f"Nie udało się dodać piłkarza {player_name}"
        self.__send_mail(subject, message)

    def __send_mail(self, subject, msg):
        from_email = "nadawca@email.com"
        recipient_list = ["odbiorca@email.com"]
        # send_mail(subject, msg, from_email, recipient_list)
        return
