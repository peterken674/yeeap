from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from decouple import config

# Tweepy
import tweepy

from time import time, sleep

consumer_key = config('CONSUMER_KEY')
consumer_secret = config('CONSUMER_SECRET')
access_token = config('ACCESS_TOKEN')
access_token_secret = config('ACCESS_SECRET')


class MainView(APIView):
    def get(self, request):
        try:    
            # Authenticate to Twitter
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)

            api = tweepy.API(auth)

            try:
                api.verify_credentials()
                # res = {'message': 'Authentication successful.'}
            except:
                res = {'message': 'Authentication failed.'}
                return Response(data=res)

            search_results = []

            for result in api.search_tweets(q='tech', lang='en', result_type='popular', count='100'):
                # tweet = {result.user.name: result.text}
                if not result.favorited and len(result.entities['hashtags']) == 0 and result.favorite_count > 20:
                    search_results.append(result) 

            count = len(search_results)

            for result in search_results:
                user_id = result.user.id
                following = api.get_friend_ids(screen_name='_peterken')

                if not result.retweeted and user_id in following:
                    api.retweet(result.id)

                print(result.favorited)
                if not result.favorited:
                    api.create_favorite(result.id, wait_on_rate_limit=True)

            res = {'message': f'{count} results'}
            search_results.clear()


            # return Response(data=res) 
        except tweepy.TooManyRequests:
            res = {'error': 'Request limit exceeded'}

        return Response(data=res)

# counter = 0
# while True:
#     sleep(15 - time() % 15)
#     print(f'Counter: {counter}')
#     main = MainView()
#     main.get()
#     counter += 1