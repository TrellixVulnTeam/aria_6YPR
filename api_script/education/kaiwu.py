# coding:utf-8
# @Time  : 2020/3/6 16:16
# @Author: Xiawang
# Description:
from utils.util import app_header_999, get_requests


def check_course_share_status(userToken, courseId):
    url = 'https://gate.lagou.com/v1/neirong/kaiwu/checkCourseShareStatus?courseId={}'.format(courseId)
    header = app_header_999(userToken=userToken, DA=False)
    remark = "言职/开悟/分享课程状态"
    return get_requests(url=url, headers=header, remark=remark)


def get_course_description(userToken, courseId):
    url = 'https://gate.lagou.com/v1/neirong/kaiwu/getCourseDescription?courseId={}'.format(courseId)
    header = app_header_999(userToken=userToken, DA=False)
    remark = "言职/开悟/查询课程描述信息"
    return get_requests(url=url, headers=header, remark=remark)


def get_distribution_info(userToken, courseId):
    url = 'https://gate.lagou.com/v1/neirong/kaiwu/getDistributionInfo?courseId={}'.format(courseId)
    header = app_header_999(userToken=userToken, DA=False)
    remark = "言职/开悟/获取分销信息"
    return get_requests(url=url, headers=header, remark=remark)

def get_course_lessons(userToken, courseId):
    url = 'https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessons?courseId={}'.format(courseId)
    header = app_header_999(userToken=userToken, DA=False)
    remark = "获取课程信息"
    return get_requests(url=url, headers=header, remark=remark)