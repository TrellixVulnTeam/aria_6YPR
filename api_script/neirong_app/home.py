# coding:utf-8
# @Time  : 2020/2/14 11:49
# @Author: Xiawang
# Description:
from utils.util import app_header_999, get_requests


def deliver_rec(userToken, ip_port=None, userId=None):
    url = 'https://gate.lagou.com/v1/neirong/home/deliverRec'
    header = app_header_999(userToken, DA=False, userId=userId)
    remark = '大家都在投'
    return get_requests(url=url, headers=header, remark=remark, ip_port=ip_port)


def fast_feedback(userToken, ip_port=None, userId=None):
    url = 'https://gate.lagou.com/v1/neirong/home/fastFeedback?pageNo=1&pageSize=10&showId=10'
    header = app_header_999(userToken, DA=False, userId=userId)
    remark = '极速反馈'
    return get_requests(url=url, headers=header, remark=remark, ip_port=ip_port)


def home_headline(userToken, ip_port=None, userId=None):
    url = 'https://gate.lagou.com/v1/neirong/home/headline?pageNo=1&pageSize=10'
    header = app_header_999(userToken, DA=False, userId=userId)
    remark = '拉勾头条列表'
    return get_requests(url=url, headers=header, remark=remark, ip_port=ip_port)


def home_page(userToken, ip_port=None, userId=None):
    url = 'https://gate.lagou.com/v1/neirong/home/page'
    header = app_header_999(userToken, DA=False, userId=userId)
    remark = 'app首页'
    return get_requests(url=url, headers=header, remark=remark, ip_port=ip_port)


def searchBySalary(userToken, ip_port=None, userId=None):
    url = 'https://gate.lagou.com/v1/neirong/home/searchBySalary'
    header = app_header_999(userToken, DA=False, userId=userId)
    remark = '薪资最高'
    return get_requests(url=url, headers=header, remark=remark, ip_port=ip_port)
