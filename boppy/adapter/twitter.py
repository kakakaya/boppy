#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: kakakaya, Date: Wed Dec  7 18:13:50 2016
import tweepy
from base import BaseInput, BaseMessage, BaseOutput
from time import sleep


class TwitterStreamListener(tweepy.StreamListener):
    def __init__(self, queue):
        self.queue = queue      # TwitterInput側と共有
        super(TwitterStreamListener, self).__init__()

    # def on_data(self, data):
    #     """Tweet受信時に発火
    #     Keyword Arguments:
    #     status -- tweet
    #     """
    #     print(data)
    #     # self.queue.append(status)

    def on_status(self, status):
        """Tweet受信時に発火
        Keyword Arguments:
        status -- tweet
        """
        print(status)
        # self.queue.append(status)

    def on_error(self, status):
        print(status)


class TwitterInput(BaseInput):
    def __init__(self, consumer_key, consumer_sec,
                 access_key, access_sec):
        """Twitterに接続し、tweepy.StreamListenerからデータを入力する。
        Keyword Arguments:
        consumer_key                 -- Twitterアクセス用。
        consumer_sec                 -- Twitterアクセス用。
        access_key                   -- Twitterアクセス用。
        access_sec                   -- Twitterアクセス用。
        """
        self.queue = []
        auth = tweepy.OAuthHandler(consumer_key, consumer_sec)
        auth.set_access_token(access_key, access_sec)
        api = tweepy.API(auth)
        self.user = api.me()
        self.stream = tweepy.Stream(auth=auth, listener=TwitterStreamListener(auth=auth, queue=self.queue))
        # self.stream.filter(async=True)

    def __next__(self):
        while not self.queue:
            sleep(0.1)          # メッセージキューが空なら待つ
        return TwitterMessage(self.queue.pop(0))


class TwitterMessage(BaseMessage):
    def __init__(self, message):
        self.message = message

    def text(self):
        return self.message.text


# temp
def main():
    ck, cs = CONSUMER_KEY, CONSUMER_SEC
    ak, as_ = ACCESS_KEY, ACCESS_SEC
    auth = tweepy.OAuthHandler(ck, cs)
    auth.set_access_token(ak, as_)
    # api = tweepy.API(auth)
    # user = api.me()
    # print(user)

    queue = []
    s = TwitterStreamListener(queue=queue)
    stream = tweepy.Stream(auth, s)
    stream.filter(track=['python'])

    """
        ti = TwitterInput(CONSUMER_KEY, CONSUMER_SEC, ACCESS_KEY, ACCESS_SEC)
    for i in ti:
        if not ti.stream.running:
            print("Stream dead")
        print(i.text())

    ti.stream.filter(track=['python'])

    """
    # l = StdOutListener()

    # stream = tweepy.Stream(auth, l)
    # stream.filter(track=['basketball'])


class StdOutListener(tweepy.StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        print(data)

    def on_error(self, status):
        print(status)


if __name__ == "__main__":
    main()
