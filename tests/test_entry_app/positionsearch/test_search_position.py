# -*- coding: utf8 -*-
__author__ = 'yqzhang'
from utils.util import assert_equal
import pytest
from api_script.entry.positionsearch.searchPosition import *

def setup_module(module):
    pass


def teardown_module(module):
    pass


def test_hrinfo():
    r=searchPositions()
    assert_equal(1, r['state'], "搜索职位成功")