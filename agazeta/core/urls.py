from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^colabore', views.index, name='index'),
    # ex: /getmatch/matchid=5/
    url(r'^matchid=(?P<matchid>[0-9]+)$', views.getmatch, name='match search'),
    # ex: /getmatch/match_year=2016-05-02/
    url(r'^match_date=(?P<year>[0-9]+)-(?P<month>[0-9]+)-(?P<day>[0-9]+)$', views.getmatch_by_date, name='match search'),
]
