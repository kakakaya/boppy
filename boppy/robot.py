#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kakakaya, Date: Mon Oct 24 15:56:33 2016
# from pprint import pprint as p
import importlib
import os
import datetime
from .adapter.base import BaseInput, BaseOutput
from .adapter.stdio import StdinInput, StdoutOutput


class Robot(object):
    def __init__(self, src, connections=[], **config):
        """
        Keyword Arguments:
        src           -- input source. i.e. sys.stdin
        connections   -- output destination. i.e. sys.stout
        conf          -- configure. (default {})
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

        # 出力先が定義されて
        self.primary_destination = None
        # 接続先のID一覧を作成してからそれぞれ接続する
        self.destinations = {}

        for c in connections:
            self.ids.append(self.connect(d))

        self.conf = config

        # 名前だけconfから取り出して初期化を行う
        # 指定されてなければ"noppy"
        self.name = self.conf.get("name", "noppy")

        # "/boppy ping"の/boppy部分を作る
        self.prefix = self.conf.get("prefix", "/"+self.name)

        # Listenerを読み込む
        self.listeners = []

        # "/boppy addtask some-task"のaddtask部分を登録する
        self.commands = {}

        # 起動時間
        self.start_time = datetime.datetime.now()

    def __str__(self):
        return '<Boppy the"{}", (src, dst)=({}, {}), {} plugins, uptime: {}>'.format(
            self.name,
            self.src.__class__.__name__,
            self.dst.__class__.__name__,
            len(self.listeners),
            self.uptime()
        )

    def uptime(self):
        return datetime.datetime.now() - self.start_time

    def connect(self, conn):
        """Robotが動作を反映させる対象となるものを接続する。
        同じサービスを複数連携させても良いが、同じ動作の対象、
        つまりユーザーを複数登録しないようにする。
        そのため、接続先に対してハッシュ化を行う。
        Keyword Arguments:
        dst -- output destination
        """
        # dst は BaseOutput から継承されていなければエラーにする
        if not issubclass(dst.__class__, BaseOutput):
            subclasses = list(dst.__class__.__bases__)
            raise Exception(
                "Robot's output destination must be subclass of BaseOutput:" +
                "This is subclass of: {}"
                .format(subclasses)
            )
        _id = dst.get_id()
        if _id in self.ids:
            raise Exception(
                "Failed to connect {}: already connected.".format(_id)
            )
        self.dst = dst
        return dst.get_id()

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
            if hasattr(plugin, "register") and callable(plugin.register):
                plugin.register(self)

    def listen(self, matcher, func):
        """If message matches by matcher, then return response by func.
        Plugins must use this function to add function for listening.
        Keyword Arguments:
        matcher -- A str, regexp or function to match input messages.
        func    -- A function to callback.
        """
        self.listeners.append(Listener(matcher, func))

    def run_command(self, msg):
        # msgをパースする
        pass

    # def respond(self, msg, text):
    #     "Robotのrespondが呼ばれた場合、srcの相手に出力することを試みる。"
    #     if msg.address:
    #         try:
    #             self.destinations[msg.address].respond(msg, text)
    #         except KeyError:
    #             pass

    # def say(self, msg, text):
    #     "Robotのsayが呼ばれた場合、最初に追加された出力先が実装するsayを行う。"
    #     self.primary_destination.say(msg, text)

    def serve(self):
        """Robotを動作させる。
        つまり、 self.src からの入力を受け取り、登録されたものに1つでもマッチしたら
        say または respond を行う。
        """
        # ジェネレータからメッセージを受け取る
        for msg in self.src:
            # prefixから始まるコマンドは優先
            if msg.text.startwith(self.prefix):
                self.run_command(msg)
            else:
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
        if not callable(callback):
            raise TypeError("callback for listener must be a function.")
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
    # 標準入力をデータ読み込み元、標準出力を
    robot = Robot(src=StdinInput(), dst=[StdoutOutput()])
    # デフォルトプラグインの読み込み
    robot.load_plugin_dir()

    # robot.serve(stream=sys.stdin)
    print(robot)
    print(list(robot.destinations.keys()))

    # 動作を開始する
    robot.serve()


if __name__ == "__main__":
    main()
