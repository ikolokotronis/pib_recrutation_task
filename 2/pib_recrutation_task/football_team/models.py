from django.db import models


class FootballClub(models.Model):
    name = models.CharField('nazwa', max_length=256)
    founded = models.DateField('data założenia')
    no_players = models.IntegerField('liczba piłkarzy')

    def __str__(self):
        return self.name


class FootballPlayer(models.Model):
    first_name = models.CharField('pierwsze imię', max_length=256)
    last_name = models.CharField('nazwisko', max_length=256)
    birth_year = models.IntegerField('rok urodzenia')
    club = models.ForeignKey(FootballClub, on_delete=models.DO_NOTHING)
    nationality = models.CharField('narodowość', max_length=256, choices=[('EU', 'EU'), ('non EU', 'non EU')])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
