# coding: utf-8
from django.views.generic import TemplateView
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from datetime import datetime, date
from models import archive, apikeys
from DoraR import test_api
from forms import ApiForm
import json


def index(request):
    if request.method == "POST":
        form = ApiForm(data=request.POST)
        username = request.POST.get("username", "")
        token = request.POST.get("token", "")
        if form.is_valid() and test_api(username, token) == True:
            form.save()
            return HttpResponse(">>> Seus dados foram salvos! </br> >>> Obrigado por ajudar a aumentar a comunidade Hearthstone!")
        else:
            return HttpResponse(">>> Seus dados não puderam ser salvos! </br> >>> Algum problema com seu username ou token")

    form = ApiForm(initial={'subscribe': True})
    return render(request, "index.html", {'form': form})


def getmatch(request, matchid):
    try:
        ret = archive.objects.filter(matchid=int(matchid))[0]
        ret = { "matchid": ret.matchid,
            #"date_posix": ret.date_posix,
            "date": ret.date.strftime("%Y-%m-%d"),
            "rank": ret.rank,
            "hero": ret.hero,
            "hero_deck": ret.hero_deck,
            "opponent_hero": ret.opponent_hero,
            "opponent_deck": ret.opponent_deck,
            "coin": ret.coin,
            "turns": ret.turns,
            "result": ret.result,
            "cards": ret.cards,
            "opponent_cards": ret.opponent_cards,
        }
    except:
        ret = {"error":404, "message": "matchid {} not found".format(matchid) }

    return JsonResponse(ret)

def getmatch_by_date(request, year, month, day):
    try:
        _date = date(int(year), int(month), int(day))
        _ret = archive.objects.filter(date=_date)
        games = []
        for ret in _ret:
            games.append( { "matchid": ret.matchid,
                "date": ret.date.strftime("%Y-%m-%d"),
                "rank": ret.rank,
                "hero": ret.hero,
                "hero_deck": ret.hero_deck,
                "opponent_hero": ret.opponent_hero,
                "opponent_deck": ret.opponent_deck,
                "coin": ret.coin,
                "turns": ret.turns,
                "result": ret.result,
                "cards": ret.cards,
                "opponent_cards": ret.opponent_cards,
            })

        ret = {"games": games, "total": len(games) }
    except Exception as e:
        print e
        ret = {"games": [], "total": 0 }

    return JsonResponse(ret)
