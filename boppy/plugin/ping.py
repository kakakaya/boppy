#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: kakakaya, Date: Mon Oct 24 16:00:13 2016
# from pprint import pprint as p
import re


def pong(msg, dst):
    dst.respond(msg, "PONG")


def register(robot):
    patt = re.compile(r"ping", re.I)
    robot.listen(patt, pong)
