from django.views.generic.edit import CreateView

from .forms import FootballPlayerForm


class AddFootballPlayerView(CreateView):
    form_class = FootballPlayerForm

    def send_mail(self, msg):
        pass
