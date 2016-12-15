#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: kakakaya, Date: Mon Oct 24 16:00:13 2016
# from pprint import pprint as p
import re


def ans(robot, msg):
    robot.respond(msg, robot.conf)


def register(robot):
    patt = re.compile(r"show config(ure)?", re.I)
    robot.listen(patt, ans)
