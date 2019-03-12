# coding:utf-8
# @Time  : 2019-03-07 20:10
# @Author: Xiawang
import pytest

from api_script.luckyshare_app.luckyShare import activity_carp_entrance, activity_carp_summary, queryRedPointType, \
    activity_carp_removeRedDot, activity_carp_queryNotes, order_interview_queryList, positions_queryList, \
    buser_hr_getList, positionCategories_get, queryPositions, queryHistoryNotes, queryInterviews, \
    activity_carp_queryNotePreview, activity_carp_publicNote, cms_luckyShare_querylist, cms_luckyShare_audit
from utils.util import assert_equal


@pytest.mark.parametrize('orderId', [(None), (0)])
def test_activity_carp_entrance(orderId):
    r = activity_carp_entrance(orderId).json()
    assert_equal(1, r['state'], "查询活动入口是否展示成功")


def test_activity_carp_summary():
    r = activity_carp_summary().json()
    assert_equal(1, r['state'], "查询活动入口是否展示成功")


@pytest.mark.parametrize('orderIds', [(''), ('1')])
def test_queryRedPointType(orderIds):
    r = queryRedPointType(orderIds).json()
    if orderIds == '':
        assert_equal(1002, r['state'], "订单编号 orderIds 的判断是否为空 正确")
    elif orderIds == '1':
        assert_equal(1, r['state'], "查询红点成功")


@pytest.mark.parametrize('type', [(1), (2), (3), (0), (4)])
def test_activity_carp_removeRedDot(type):
    r = activity_carp_removeRedDot(type)
    if 1 <= type <= 3:
        assert_equal(1, r['state'], "消除红点成功")
    else:
        assert_equal(1002, r['state'], "对异常红点类型的处理正确")


@pytest.mark.parametrize('category1, category2, category3', [('开发|测试|运维类', '后端开发', 'Java')])
def test_activity_carp_queryNotes(category1, category2, category3):
    r = activity_carp_queryNotes(category1, category2, category3).json()
    assert_equal(1, r['state'], "查询帖子列表成功")


def test_queryInterviews():
    # todo  获取订单id
    r = queryInterviews().json()
    assert_equal(1, r['state'], "查询历史晒贴")


@pytest.mark.parametrize('ids', [(''), (None)])
def test_order_interview_queryList(ids):
    # todo 缺失订单id，待从面试列表查询
    r = order_interview_queryList(ids).json()
    if not (ids == None):
        assert_equal(1002, r['state'], "对订单编号为空的处理正确")
    else:
        assert_equal(1, r['state'], "单独及批量查询面试订单成功")


@pytest.mark.parametrize('ids', [(''), (None)])
def test_positions_queryList(ids):
    r = positions_queryList(ids).json()
    if not (ids == None):
        assert_equal(1002, r['state'], "对职位id为空的处理正确")
    else:
        assert_equal(1, r['state'], "单独及批量查询职位成功")


def test_queryPositions():
    r = queryPositions()
    assert_equal(1, r['state'], "查询曝光职位成功")


def test_queryHistoryNotes():
    r = queryHistoryNotes().json()
    assert_equal(1, r['state'], "查询历史晒贴")


def test_activity_carp_queryNotePreview():
    r = activity_carp_queryNotePreview().json()
    assert_equal(1, r['state'], "查询发帖前的预览信息")


@pytest.mark.parametrize('content, userName', [('测试发帖了', '小宸')])
def test_activity_carp_publicNote(content, interviewId, userName):
    r = activity_carp_publicNote(content, interviewId, userName)
    assert_equal(1, r['state'], "发帖成功")


def test_cms_luckyShare_querylist(login_home_k8s_default):
    # todo 差登录没处理1
    r = cms_luckyShare_querylist().json()
    assert_equal(True, r['success'], "home后台锦鲤贴列表查询成功")


def test_cms_luckyShare_audit(login_home_k8s_default):
    # todo 差登录没处理2
    r = cms_luckyShare_audit()
    assert_equal(True, r['success'], "home后台锦鲤贴列表查询成功")
