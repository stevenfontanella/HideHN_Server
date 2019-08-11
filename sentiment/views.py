from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse

import requests

'''
right to left composition for unary functions
'''
def compose(*fns):
    def inner(x):
        curr = x
        for f in reversed(fns):
            curr = f(curr)
        return curr
    return inner

def get_hn_post(id):
    # TODO: validate id

    # https://stackoverflow.com/questions/30967822/when-do-i-use-path-params-vs-query-params-in-a-restful-api

    # this is a bottleneck, but much faster than loading the actual website
    # with post caching it should be reasonable
    # hn = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json").json()
    return None

    return hn

a = True
def should_filter(json):
    global a
    a ^= True
    return a

def index(request):
    try:
        ids = request.GET.getlist("id")
        print(ids)
    except KeyError:
        return HttpResponseBadRequest("No ids given")

    sentiment_list = list(map(compose(int, should_filter, get_hn_post), ids))
    print(sentiment_list)

    return JsonResponse(sentiment_list, safe=False)

