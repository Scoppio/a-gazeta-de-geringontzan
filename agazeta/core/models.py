from __future__ import unicode_literals

from django.db import models

class apikeys(models.Model):
    SERVERS = (
        ('a', 'Americas'),
        ('e', 'Europa'),
        ('c', 'Asia'),
    )
    username = models.CharField(max_length=50)
    token = models.CharField(max_length=80)
    server = models.CharField(max_length=50, choices=SERVERS, default=SERVERS[0])
    email = models.EmailField(blank=True, null=True)
    subscribe = models.BooleanField()
    validToken = models.BooleanField(default=True)
    class Meta:
        unique_together = ['username', 'token']

    def __str__(self):
        return self.username

class archive(models.Model):
    matchid = models.IntegerField(unique=True)
    date_posix = models.IntegerField(blank=True, null=True)
    date = models.DateField()
    rank = models.IntegerField(blank=True, null=True)
    hero = models.CharField(max_length=20)
    hero_deck = models.CharField(max_length=100,blank=True, null=True)
    opponent_hero = models.CharField(max_length=20, blank=True)
    opponent_deck = models.CharField(max_length=100, blank=True, null=True)
    coin = models.BooleanField()
    turns = models.IntegerField(blank=True, null=True)
    result = models.BooleanField()
    cards = models.TextField(blank=True, null=True)
    opponent_cards = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.matchid)
