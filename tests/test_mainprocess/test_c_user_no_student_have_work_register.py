# coding:utf-8
# @Time  : 2019-09-20 17:59
# @Author: Xiawang
# Description:

import time

import pytest

from api_script.entry.account.me import bing_or_change_phone
from api_script.entry.account.passport import password_login, send_verify_code, verifyCode_login, register_by_phone, \
    get_login_by_token
from api_script.entry.cuser.baseStatus import get_info
from api_script.neirong_app.resumes import guideBasicInfo, educationExperiences, personalCards, abilityLabels, \
    expectJob, workExperiences, set_basicInfo, delete_education_experiences, get_detail, delete_workExperiences
from utils.util import assert_equal, verify_code_message

countryCode, phone = "00852", str(20000000 + int(str(time.time()).split('.')[1]))


def test_send_verify_code():
    r = send_verify_code(countryCode, phone, "PASSPORT_REGISTER")
    assert_equal(1, r['state'], '校验发送验证码成功', "校验发送验证码失败")


time.sleep(2)

def test_get_verify_code():
    global verify_code
    verify_code = verify_code_message(countryCode, phone)
    assert_equal(True, bool(verify_code), "校验获取验证码成功")


def test_verifyCode_login():
    r = verifyCode_login(countryCode, phone, verify_code)
    assert_equal(201001, r['state'], "校验验证码登录转注册成功")


def test_register_by_phone():
    r = register_by_phone(countryCode, phone, verify_code)
    assert_equal(1, r['state'], "校验注册成功")
    global userToken
    userToken = r['content']['userToken']


def test_get_login_by_token():
    r = get_login_by_token(userToken)
    assert_equal(1, r['state'], '校验token登录成功')


def test_guideBasicInfo():
    r = guideBasicInfo(countryCode + phone, 2, userToken)
    assert_equal(1, r['state'], '校验提交基本信息成功')


def test_workExperiences():
    r = workExperiences(userToken, )
    assert_equal(1, r['state'], '校验提交工作经历')


def test_educationExperiences():
    r = educationExperiences(userToken)
    assert_equal(1, r['state'], "校验提交教育经历成功")


def test_personalCards():
    r = personalCards(userToken)
    assert_equal(1, r['state'], '校验提交个人名片成功')


def test_abilityLabels():
    r = abilityLabels(userToken)
    assert_equal(1, r['state'], '校验提交综合能力成功')


def test_expectJob():
    r = expectJob(userToken)
    assert_equal(1, r['state'], '校验提交求职意向')


def test_get_info():
    r = get_info(userToken)
    assert_equal(1, r['state'], '获取C端用户信息')


countryCode_change, phone_change = "00852", str(20000000 + int(str(time.time()).split('.')[1]))


def test_change_phone_send_verify_code():
    r = send_verify_code(countryCode_change, phone_change, "RESUME_CHANGE_BIND_PHONE")
    assert_equal(1, r['state'], '校验发送验证码成功')


def test_update_phone_get_verify_code():
    global verify_code
    verify_code = verify_code_message(countryCode_change, phone_change)
    assert_equal(True, bool(verify_code), "校验获取验证码成功")


def test_change_phone():
    r = bing_or_change_phone(userToken, countryCode_change, phone_change, verify_code)
    assert_equal(1, r['state'], "校验绑定新手机号成功！")


def test_get_detail():
    r = get_detail(userToken)
    assert_equal(1, r['state'], "校验获取简历详情页面成功")
    global ed_id, wk_id
    ed_id = r['content']['educationExperiences'][0]['id']
    wk_id = r['content']['workExperiences'][0]['id']


def test_delete_education_experiences():
    r = delete_education_experiences(userToken, ed_id)
    assert_equal(2105005, r['state'], '校验删除唯一段教育经历成功')


@pytest.mark.parametrize("schoolName,education,startDate,endDate",
                         [('清华大学', '硕士', '2014', '2017')])
def test_update_educationExperiences(schoolName, education, startDate, endDate):
    r = educationExperiences(userToken=userToken, schoolName=schoolName, education=education, startDate=startDate,
                             endDate=endDate)
    assert_equal(1, r['state'], '校验增加一段教育经历成功')


def test_delete_education_experiences_2():
    r = delete_education_experiences(userToken, ed_id)
    assert_equal(1, r['state'], '校验删除一段教育经历成功')


def test_delete_workExperiences():
    r = delete_workExperiences(userToken, wk_id)
    assert_equal(2105005, r['state'], '校验删除唯一段工作经历成功')


@pytest.mark.parametrize("companyName,startDate,endDate", [("阿里巴巴集团钉钉事业部", "2013.07", "2015.09")])
def test_update_workExperiences(companyName, startDate, endDate):
    r = workExperiences(userToken, companyName=companyName, startDate=startDate, endDate=endDate)
    assert_equal(1, r['state'], '校验增加一段工作经历成功')


def test_delete_workExperiences_2():
    r = delete_workExperiences(userToken, wk_id)
    assert_equal(1, r['state'], '校验删除一段工作经历成功')