#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: kakakaya, Date: Mon Oct 24 13:25:35 2016
# from pprint import pprint as p
import datetime
import re


def check_xmas():
    now = datetime.datetime.now()
    if (now.month, now.day) == (12, 25):
        return True
    else:
        return False


def is_xmas(msg, dst):
    ans = ""
    if check_xmas():
        ans = "YES"
    else:
        ans = "NO"
    dst.respond(msg, ans)


def register(robot):
    robot.listen(re.compile("is it xmas\?", re.I), is_xmas)
