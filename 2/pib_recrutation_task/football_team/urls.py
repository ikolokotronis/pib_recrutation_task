
from django.contrib import admin
from django.urls import path

from .views import AddFootballPlayerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('players/', AddFootballPlayerView.as_view(), name='add_player')
]
