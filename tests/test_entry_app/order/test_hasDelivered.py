# -*- coding: utf8 -*-
__author__ = 'yqzhang'

from utils.util import assert_equal
import pytest
from api_script.entry.order.hasDelivered import *

def setup_module(module):
    pass


def teardown_module(module):
    pass


def test_hasDelivered():
    r=hasDelivered()
    assert_equal(1, r['content']['5378018'], "职位已投递")