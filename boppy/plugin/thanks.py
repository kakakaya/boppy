#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: kakakaya, Date: Sun Nov  6 00:47:26 2016
# from pprint import pprint as p
import re
from random import choice


response = [
    "you're welcome",
    "no problem",
    "not a problem",
    "no problem at all",
    "don’t mention it",
    "it’s no bother",
    "it’s my pleasure",
    "my pleasure",
    "it’s nothing",
    "think nothing of it",
    "no, no. thank you!",
    "sure thing",
    "どういたしまして",
    "気にするな",
    "またなにかあればどうぞ",
]


def resp(robot, msg):
    robot.dst.respond(msg, choice(response))


def register(robot):
    robot.listen(re.compile(r"thanks?", re.I), resp)
