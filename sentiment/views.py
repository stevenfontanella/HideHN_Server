from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core.cache import cache

from sentiment.models import Post

import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import multiprocessing as mp
import logging

log = logging.getLogger(__name__)
sentiment_analyzer = SentimentIntensityAnalyzer()

'''
return json object for an HN post 
'''
def get_hn_post(id):
    # TODO: validate id

    hn = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json").json()
    return hn

def sentiment(id):
    json = get_hn_post(id)
    title = json["title"]

    return sentiment_analyzer.polarity_scores(title)["compound"]

def id_to_record(id):
    return Post(id, sentiment(id))

def index(request):
    log.info("Got request: %s", request)

    ids = list(map(int, request.GET.getlist("id")))
    sentiments = Post.objects.in_bulk(ids)

    missing = list(filter(lambda x: x not in sentiments, ids))
    with mp.Pool() as pool:
        new_posts = pool.map(id_to_record, missing)

        # these lines are needed, otherwise the context manager __exit__ hangs
        # pool.close()
        # pool.join()
    sentiments.update(zip(missing, new_posts))

    # if there was a conflict, then another request must have caused the entry to be added
    # so there's not issue; we can just ignore it
    Post.objects.bulk_create(new_posts)
    # sentiments = Post.objects.in_bulk(ids)

    sentiment_list = map(lambda id: int(sentiments[id].sentiment < 0), ids)
    # sentiment_list = map(lambda post: post.sentiment < 0, Post.objects.in_bulk(ids))
    # safe=False to send a list
    return JsonResponse(list(sentiment_list), safe=False)
