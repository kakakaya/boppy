#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: kakakaya, Date: Mon Oct 24 16:00:13 2016
# from pprint import pprint as p
import re


def ans(robot, msg):
    robot.dst.respond(msg, robot.name)


def register(robot):
    patt = re.compile(r"your name", re.I)
    robot.listen(patt, ans)
