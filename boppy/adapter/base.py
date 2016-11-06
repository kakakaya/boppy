#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: kakakaya, Date: Sun Nov  6 21:05:48 2016
# from pprint import pprint as p
from abc import ABCMeta, abstractmethod


class BaseInput(object, metaclass=ABCMeta):
    """標準入力、Slack、Twitter UserStreamなどの連続したデータを読み込む対象。
    __next__ メソッドを必ず実装する。
    """
    def __init__(self):
        pass

    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self):
        """
        """
        raise NotImplementedError("{} class has not implemented __next__ method yet.".format(self.__class__))


class BaseMessage(object, metaclass=ABCMeta):
    """BaseInputを継承した入力元から送出される一つのデータの塊。
    例えば、標準入力における1行など。
    コンテキスト的なものが必要だったりするので、このクラスを継承する
    """
    def __init__(self):
        pass

    @abstractmethod
    def text(self):
        """データにおけるテキスト部分。
        発言における本文など。
        必ず実装する。
        """
        raise NotImplementedError("{} class has not implemented text method yet.".format(self.__class__))


class BaseOutput(object, metaclass=ABCMeta):
    """Robot が結果を出力する対象。
    """

    @abstractmethod
    def say(self, message, **kwargs):
        """そのまま出力する場合、sayを使用する。
        """
        raise NotImplementedError("{} class has not implemented say method yet.".format(self.__class__))

    @abstractmethod
    def respond(self, message, **kwargs):
        """相手を明確にして出力する(返信など)場合、respondを使用する。
        """
        raise NotImplementedError("{} class has not implemented respond method yet.".format(self.__class__))
