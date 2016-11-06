#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kakakaya, Date: Mon Oct 24 15:56:33 2016
# from pprint import pprint as p
import importlib
import os
import datetime
from adapter.base import BaseInput, BaseOutput
from adapter.stdio import StdinInput, StdoutOutput


class Robot(object):
    def __init__(self, src, dst, conf={}):
        """
        Keyword Arguments:
        src   -- input source. i.e. sys.stdin
        dst   -- output destination. i.e. sys.stout
        conf  -- configure. (default {})
        """
        # src は BaseInput から継承されていなければエラーにする
        if issubclass(src.__class__, BaseInput):
            self.src = src
        else:
            subclasses = list(src.__class__.__bases__)
            raise Exception(
                "Robot's input source must be subclass of BaseInput:" +
                "This is subclass of: {}"
                .format(subclasses)
            )
        # dst は BaseOutput から継承されていなければエラーにする
        if issubclass(dst.__class__, BaseOutput):
            self.dst = dst
        else:
            subclasses = list(dst.__class__.__bases__)
            raise Exception(
                "Robot's output destination must be subclass of BaseOutput:" +
                "This is subclass of: {}"
                .format(subclasses)
            )

        self.conf = conf

        # 名前だけconfから取り出して初期化を行う
        if self.conf.get("name"):
            self.name = self.conf["name"]
        else:
            self.name = "Noppy"  # nice name?

        # Listenerを読み込む
        self.listeners = []

        # 起動時間
        self.start_time = datetime.datetime.now()

    def __str__(self):
        return '<Boppy named "{}", (src, dst)=({}, {}), {} plugins, uptime: {}>'.format(
            self.name,
            self.src.__class__.__name__,
            self.dst.__class__.__name__,
            len(self.listeners),
            self.uptime()
        )

    def uptime(self):
        return datetime.datetime.now() - self.start_time

    def load_plugin_dir(self, plugin_dir="plugin"):
        """指定されたディレクトリ内の.pyファイルを全て読み込む
        """
        plugins = []
        for f in os.listdir(plugin_dir):
            if f.endswith(".py"):
                mod_path = str(plugin_dir+"."+f).rstrip(".py")
                # print(mod_path)
                plugins.append(importlib.import_module(
                    mod_path
                ))

        for plugin in plugins:
            # 各プラグインは必ずregister関数を持つ
            plugin.register(self)

    def listen(self, matcher, func):
        """If message matches by matcher, then return response by func.
        Plugins must use this function to add function for listening.
        Keyword Arguments:
        matcher -- A str, regexp or function to match input messages.
        func    -- A function to callback.
        """
        self.listeners.append(Listener(matcher, func))

    def serve(self):
        """Robotを動作させる。
        つまり、 self.src からの入力を受け取り、登録されたものに1つでもマッチしたら
        say または respond を行う。
        """
        for msg in self.src:
            for listener in self.listeners:
                if listener.match(msg):
                    listener.react(self, msg)
                    # 一回動作したらそのメッセージについては動作しない
                    break


class Listener(object):
    """Robot がlistenする表現や関数と、コールバック関数の組。
    """
    def __init__(self, pattern, callback):
        """
        Keyword Arguments:
        pattern  -- 文字列、コンパイルされた正規表現、関数のいずれか
        callback -- patternがメッセージと一致した場合に返される
        """
        self.pattern = pattern
        self.callback = callback

    def match(self, msg):
        """
        Keyword Arguments:
        msg -- message to check it matches this or not
        """
        if callable(self.pattern):
            # 関数なので、msgを引数にして呼び出してみる
            return self.pattern(msg)
        elif type(self.pattern) is str:
            # 文字列なので、直接比較する
            return self.pattern == msg.text()
        elif getattr(self.pattern, "match", False):
            # 正規表現っぽいので、matchさせてみる
            return self.pattern.match(msg.text())
        else:
            # pattern が変
            raise Exception("Robot is listening odd pattern {}: must be str, regexp, or function.".format(
                self.pattern.__class__.__name__
            ))

    def react(self, robot, msg):
        """
        Keyword Arguments:
        robot -- who react for msg
        msg   -- msg to work for
        """
        self.callback(robot, msg)


def main():
    robot = Robot(src=StdinInput(), dst=StdoutOutput())
    robot.load_plugin_dir()

    # robot.serve(stream=sys.stdin)
    print(robot)
    robot.serve()

if __name__ == "__main__":
    main()
