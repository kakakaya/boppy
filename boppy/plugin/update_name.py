#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: kakakaya, Date: Thu Dec  8 13:20:27 2016
# from pprint import pprint as p

command = "update_name"


def update_name(robot, msg):
    if hasattr(robot.src, "update_name") and callable(robot.src.update_name):
        new_name = msg.replace(command, "").strip()  # 再帰による攻撃を防ぐため、全部取り除く
        robot.src.update_name(new_name)


def register(robot):
    robot.listen(command, update_name)
