from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core.cache import cache

import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import multiprocessing

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

'''
Lookup the key, or else add the corresponding value to the cache and return it
@fn - function from key to value
'''
def get_cache_or_else(key, fn):
    val = cache.get(key)
    if val is None:
        val = fn(key)
        cache.set(key, val)

    return val

'''
return json object for an HN post 
'''
def get_hn_post(id):
    # TODO: validate id

    # https://stackoverflow.com/questions/30967822/when-do-i-use-path-params-vs-query-params-in-a-restful-api

    # this is a bottleneck, but much faster than loading the actual website
    # with post caching it should be reasonable
    hn = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json").json()

    return hn

def should_filter(json):
    title = json["title"]

    sentiment_analyzer = SentimentIntensityAnalyzer()
    sent = sentiment_analyzer.polarity_scores(title)

    is_filter = sent["compound"] < 0
    if is_filter:
        print(f"Filtered: {json['title']}")

    return is_filter

def id_to_bool(id):
    return get_cache_or_else(id, compose(int, should_filter, get_hn_post))

def index(request):
    try:
        ids = request.GET.getlist("id")
    except KeyError:
        return HttpResponseBadRequest("No ids given")

    with multiprocessing.Pool() as pool:
        sentiment_list = list(pool.map(id_to_bool, ids))

    return JsonResponse(sentiment_list, safe=False)

