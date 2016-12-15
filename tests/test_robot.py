#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: kakakaya, Date: Thu Dec 15 13:14:32 2016
# from pprint import pprint as p
from unittest import TestCase
from nose.tools import ok_, eq_, raises
from boppy import robot
from boppy.adapter.stdio import StdinInput, StdoutOutput


class TestRobot(TestCase):
    def setUp(self):
        self.robot = robot.Robot(src=StdinInput(), dst=[StdoutOutput()])

    def test_init(self):
        ok_(self.robot)
