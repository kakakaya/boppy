#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: kakakaya, Date: Sun Nov  6 00:47:26 2016
# from pprint import pprint as p


def resp(robot, msg):
    robot.dst.respond(msg, robot.uptime())


def register(robot):
    robot.listen("uptime", resp)
