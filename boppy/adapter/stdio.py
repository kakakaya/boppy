#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: kakakaya, Date: Sun Nov  6 21:02:12 2016
# from pprint import pprint as p
import sys
from .base import BaseInput, BaseMessage, BaseOutput


class StdinInput(BaseInput):
    def __next__(self):
        """標準入力から1行を受け取り、末尾の改行を取り除いて返す例
        """
        return StdinMessage(sys.stdin.readline().rstrip("\n"))


class StdinMessage(BaseMessage):
    def __init__(self, text):
        self._text = text
        self.address = "stdout"  # 標準入力からのメッセージに返信をするには標準出力が適切であるので、"stdout"を返す。

    @property
    def text(self):
        return self._text


class StdoutOutput(BaseOutput):
    def __init__(self):
        self.name = "stdout"

    def say(self, message, text):
        print(text)

    def respond(self, message, text):
        print(text)
