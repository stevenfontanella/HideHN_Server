from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest

import requests

def get_hn_post(id):
    # TODO: validate id
    # TODO: id should be part of path, not param
    # https://stackoverflow.com/questions/30967822/when-do-i-use-path-params-vs-query-params-in-a-restful-api

    # hn = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json").json()

    ...
    # print(hn)

a = True
def should_filter(json):
    global a
    a ^= True
    return a

def index(request):
    try:
        id = request.GET["id"]
    except KeyError:
        return HttpResponseBadRequest("No id given")

    json = get_hn_post(id)
    should = int(should_filter(json))
    print(should)
    return HttpResponse(should)

