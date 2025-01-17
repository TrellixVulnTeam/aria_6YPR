# @Author: Xiawang
# Description:
import datetime
import pytest

from api_script.education.app import get_homepage_cards, get_all_course_purchased_record, get_course_baseinfo
from api_script.education.bigcourse import get_course_info, get_course_outline, get_week_lessons, get_watch_percent, \
    no_class_dacourse
from api_script.education.course import get_course_commentList, get_distribution_poster_data, get_credit_center_info, \
    get_distribution_course_list, get_my_earing, get_user_earnings_detail, get_wei_xin_user, get_course_credit_info, \
    receive_credit, exchange_present
from api_script.education.kaiwu import get_course_description, get_distribution_info, check_course_share_status, \
    get_course_lessons, ice_breaking_location, save_course_history, get_lesson_play_history, ice_breaking_html, \
    get_course_history
from api_script.entry.account.me import modify_password
from api_script.entry.account.passport import send_verify_code, register_by_phone, verifyCode_login
from api_script.entry.cuser.baseStatus import batchCancel
from utils.util import assert_equal, assert_in, get_verify_code_message_len, assert_not_equal, verify_code_message
from api_script.education.edu import get_course_list,get_content_list,get_promotion_list,get_pop_dialog,get_course_list_only_for_member,draw_Course
import random


@pytest.mark.incremental
class TestEducation01(object):

    def test_get_homepage_cards(self, c_login_education_022601):
        r = get_homepage_cards(userToken=c_login_education_022601[0])
        assert_equal(1, r.get('state'), "拉勾教育-获取首页卡片信息列表用例通过", te='张红彦')
        global first_small_course_id, first_small_course_brief, first_small_course_title, decorate_id
        first_small_course_id = r['content']['pageCardList'][2]['smallCourseList'][0]['id']
        first_small_course_brief = r['content']['pageCardList'][2]['smallCourseList'][0]['brief']
        first_small_course_title = r['content']['pageCardList'][2]['smallCourseList'][0]['title']
        decorate_id = r['content']['pageCardList'][2]['smallCourseList'][0]['decorateId']

    def test_check_course_share_status(self, c_login_education_022601):
        r = check_course_share_status(userToken=c_login_education_022601[0], courseId=first_small_course_id)
        assert_equal(1, r.get('state'), "选课查询课程详情用例通过", te='张红彦')

    def test_get_course_lessons(self, c_login_education_022601):
        r = get_course_lessons(userToken=c_login_education_022601[0], courseId=first_small_course_id)
        assert_equal(first_small_course_id, r['content']['courseSectionList'][0]['courseId'], '查询课程详情用例通过', te='张红彦')

    def test_get_course_description(self, c_login_education_022601):
        r = get_course_description(userToken=c_login_education_022601[0], courseId=first_small_course_id)
        assert_equal(first_small_course_id, r['content']['id'], "选课查询课程详情用例通过", te='张红彦')

    def test_get_distribution_info(self, c_login_education_022601):
        r = get_distribution_info(userToken=c_login_education_022601[0], courseId=first_small_course_id,
                                  decorateId=decorate_id)
        assert_equal(1, r.get('state'), '言职/开悟/获取分销信息用例通过', te='张红彦')
        if r['content']['showDistributionButton'] is True:
            assert_equal(first_small_course_brief, r['content']['distributionBaseInfoVo']['brief'], "该课程有分销信息用例通过",
                         te='张红彦')

    def test_get_course_commentList(self, c_login_education_022601):
        r = get_course_commentList(userToken=c_login_education_022601[0], courseId=first_small_course_id)
        assert_equal(1, r.get('state'), "获取课程的评论用例通过", te='张红彦')


    def test_get_distribution_poster_data(self, get_h5_token):
        r = get_distribution_poster_data(courseId=first_small_course_id, decorateId=decorate_id,
                                         gateLoginToken=get_h5_token)
        assert_equal(first_small_course_title, r['content']['courseName'], "获取分销海报数据用例通过", te='张红彦')


@pytest.mark.incremental
class TestEducation02(object):
    def test_get_all_course_purchased_record(self, c_login_education_022601):
        r = get_all_course_purchased_record(userToken=c_login_education_022601[0])
        assert_equal(1, r.get('state'), "获取所有已购课程的列表(大课和专栏课程)用例通过", te='张红彦')
        global big_course_record_id, small_course_record_id
        big_course_record_id = r['content']['allCoursePurchasedRecord'][0]['bigCourseRecordList'][0]['id']
        small_course_record_id = r['content']['allCoursePurchasedRecord'][1]['courseRecordList'][0]['id']
        identityCode = r['content']['memberAdsBar']['identityCode']

    def test_get_course_info(self, c_login_education_022601):
        r = get_course_info(userToken=c_login_education_022601[0], courseId=big_course_record_id)
        assert_equal(1, r.get('state'), "获取大课的课程基本信息用例通过", te='张红彦')
        global lastWatchWeekId
        lastWatchWeekId = r['content']['lastWatchWeekId']

    def test_get_course_outline(self, c_login_education_022601):
        r = get_course_outline(userToken=c_login_education_022601[0], courseId=big_course_record_id)
        assert_equal(1, r.get('state'), "获取大课的课程大纲用例通过", te='张红彦')

    def test_get_week_lessons(self, c_login_education_022601):
        r = get_week_lessons(userToken=c_login_education_022601[0], courseId=big_course_record_id, weekId=lastWatchWeekId)
        assert_equal("SUCCESS", r['content']['bigCourseResult'], "获取大课一周下的所有课时用例通过", te='张红彦')

    def test_get_watch_percent(self, c_login_education_022601):
        r = get_watch_percent(userToken=c_login_education_022601[0], courseId=big_course_record_id, weekId=lastWatchWeekId)
        assert_equal(1, r.get('state'), "获取大课一周录播视频观看进度", te='张红彦')



def test_get_credit_center_info(c_login_education_022601):
    r = get_credit_center_info(userToken=c_login_education_022601[0])
    assert_equal(1, bool(len(r.get('content').get('userGrowthCreditTaskVos'))), "学分中心任务列表", te='张红彦')



def test_get_course_credit_info(c_login_education_022601):
    x = TestEducation02()
    x.test_get_all_course_purchased_record(c_login_education_022601)
    r = get_course_credit_info(userToken=c_login_education_022601[0], courseId=small_course_record_id)
    assert_equal(1, bool(len(r.get('content').get('userGrowthCreditTaskVos'))), "个人成就的任务列表", te='张红彦')



def test_ice_breaking_location():
    r = ice_breaking_location()
    assert_equal("限时1元抢>", r['content']['text'], "显示1元购入口", te='张红彦')


def test_ice_breaking_html():
    r = ice_breaking_html()
    assert_in("拉勾教育首购用户【1元抢好课】", r, "进入到1元购的界面", te='张红彦')




@pytest.mark.incremental
class TestEducationhistory(object):
    def test_get_course_list(self, c_login_education_022601):
        r = get_course_list(userToken=c_login_education_022601[0])
        assert_equal(True, bool(r), "从选课页获取已购买课程成功", te='张红彦')
        global hasbuy_small_course_id
        hasbuy_small_course_id = r[1][-1]

    def test_get_content_list(self, c_login_education_022601):
        r = get_content_list(userToken=c_login_education_022601[0])
        assert_equal("训练营",r['content']['contentCardList']['cardTitle'],'获取训练营内容列表专区数据用例通过',te='张红彦')

    def test_get_promotion_list(self,c_login_education_022601):
        r = get_promotion_list(userToken=c_login_education_022601[0])
        assert_equal("广告banner", r['content']['promotionCardList'][0]['cardTitle'], '获取推广促销活动列表专区数据用例通过', te='张红彦')


    def test_get_course_baseinfo(self, c_login_education_022601):
        r = get_course_baseinfo(hasbuy_small_course_id, userToken=c_login_education_022601[0])
        assert_equal(hasbuy_small_course_id, r['content']['courseId'], "获取课程学习基本信息用例通过", te='张红彦')
        global sectionId, lessonId
        sectionId = r['content']['lastLearnSectionId']
        lessonId = r['content']['lastLearnLessonId']

    def test_get_lesson_play_history(self, get_h5_token):
        r = get_lesson_play_history(lessonId, gateLoginToken=get_h5_token)
        assert_equal(hasbuy_small_course_id, r['content']['courseId'], "获取课时播放历史记录", te='张红彦')
        global historyHighestNode
        historyHighestNode = r['content']['historyHighestNode']

    def test_save_course_history(self, get_h5_token):
        mediaType = random.randint(0, 2)
        historyNode = random.randint(1, historyHighestNode)
        r = save_course_history(hasbuy_small_course_id, sectionId, lessonId, mediaType, historyNode,
                                gateLoginToken=get_h5_token)
        assert_equal(1, r['state'], "保存课程下课时的历史节点", te='张红彦')

    def test_get_distribution_course_list(self,get_h5_token):
        r = get_distribution_course_list(gateLoginToken=get_h5_token)
        assert_equal(1, bool(r.get('content').get('distributionCourseList')), "获取分销列表用例通过", te='张红彦')


    def test_get_my_earing(self,get_h5_token):
        r = get_my_earing(gateLoginToken=get_h5_token)
        assert_equal(1, bool(r['content']['availableEarning']), "获取我的收益用例通过", te='张红彦')


    def test_get_user_earnings_detail(self,get_h5_token):
        r = get_user_earnings_detail(gateLoginToken=get_h5_token)
        assert_equal(1, bool(r['content']['unavailableEarning']), "获取收益详情用例通过", te='张红彦')


    def test_get_wei_xin_user(self,get_h5_token):
        r = get_wei_xin_user(gateLoginToken=get_h5_token)
        assert_equal(True, r['content']['hasBind'], "获取微信用户信息用例通过", te='张红彦')


now_time = datetime.datetime.now()
minute = now_time.minute


def test_is_verify_code_reach_upper_limit():
    global send_verify_code_times
    countryCode, phone = "0044", "2020070700"
    send_verify_code_times = get_verify_code_message_len(countryCode, phone)
    assert_not_equal(-1, send_verify_code_times, '获取验证码用例通过', te='张红彦')


@pytest.mark.incremental
@pytest.mark.skipif('send_verify_code_times>=50 or minute % 2==0', reason='验证码超过50次并且是偶数分钟跳过用例')
# class TestUserGrowth(object):
#     def test_receive_credit1(self, c_login_education_0044, get_edu_h5_token):
#         global receive_success
#         r = receive_credit(gateLoginToken=get_edu_h5_token)
#         receive_success = r.get('content')
#         assert_equal(1, r.get('state'), "领取学分接口请求成功", te='张红彦')
#
#     def test_exchange_present1(self, get_edu_h5_token, c_login_education_0044):
#         if receive_success == 1:
#             change1 = exchange_present(gateLoginToken=get_edu_h5_token)
#             assert_equal(1, change1.get('state'), "领取登录学分后，兑换成功", te='张红彦')
#
#     def test_usable_credit(self, c_login_education_0044, get_edu_h5_token):
#         global courseCredit
#         r = get_credit_center_info(userToken=c_login_education_0044[0])
#         courseCredit = r.get('content').get('usableCredit')
#         assert_equal(1, r.get('state'), "获取可用学分执行成功", te='张红彦')
#
#     def test_exchange_present2(self, get_edu_h5_token):
#         if courseCredit != 0:
#             change2 = exchange_present(gateLoginToken=get_edu_h5_token)
#             assert_equal(1, change2.get('state'), "利用现有学分余额兑换成功", te='张红彦')
#
#     def test_batch_register(self, c_login_education_0044):
#         userid = c_login_education_0044[1]
#         batch_state = batchCancel(userIds=userid)
#         assert_equal(1, batch_state.get('state'), "账号注销成功", te='张红彦')
#
#         countrycode_phone = c_login_education_0044[2]
#         countrycode = countrycode_phone[1:5]
#         phone = countrycode_phone[5:]
#         sendverigycode = send_verify_code(countryCode=countrycode, phone=phone, businessType='PASSPORT_REGISTER',
#                                           app_type='LGEdu')
#         assert_equal(1, sendverigycode.get('state'), "验证码发送成功", te='张红彦')
#
#         verify_code = verify_code_message(countryCode=countrycode, phone=phone)
#         assert_equal(True, bool(verify_code), "获取验证码成功", te='张红彦')
#
#         verifyCode_login(countryCode=countrycode, phone=phone, verify_code=verify_code, app_type='LGEdu')
#         registate = register_by_phone(countryCode=countrycode, phone=phone, verify_code=verify_code, app_type='LGEdu')
#         assert_equal(1, registate.get('state'), "账号注册成功", te='张红彦')
#
#         retoken = register_by_phone(countryCode=countrycode, phone=phone, verify_code=verify_code, app_type='LGEdu')
#         m = modify_password(userToken=retoken.get('content').get('userToken'))
#         assert_equal(1, m['state'], "设置密码成功", te='张红彦')
#
#     def test_get_course_history(self, get_h5_token):
#         r = get_course_history(hasbuy_small_course_id, gateLoginToken=get_h5_token)
#         assert_equal(1, r['state'], "获取课程历史记录", te='张红彦')

    # def test_get_course_history(self, get_h5_token):
    #     r = get_course_history(hasbuy_small_course_id, gateLoginToken=get_h5_token)
    #     assert_equal(1, r['state'], "获取课程历史记录", te='张红彦')


# def test_dake_no_class(dake_no_class):
#     r = no_class_dacourse()
#     assert_equal("联系课程顾问加入班级", r['content']['allCoursePurchasedRecord'][0]['bigCourseRecordList'][0]['prepayTip'],
# <<<<<<< HEAD
#                  "暂未进班", te='betty')
#     assert_equal("训练营", r['content']['allCoursePurchasedRecord'][0]['title'], "有训练营课程", te='betty')

@pytest.mark.incremental
class Testmember(object):
    def test_get_pop_dialog(self, c_login_education_022601):
        r = get_pop_dialog(userToken=c_login_education_022601[0])
        assert_equal(1, r['content']['identityCode'], "拉勾教育会员/会员弹窗测试用例通过", te='张红彦')

    def test_get_course_list_only_for_member(self,get_h5_token):
        r = get_course_list_only_for_member(gateLoginToken=get_h5_token)
        assert_equal(1, r['content']['identityCode'], "拉勾教育会员/获取用户简单信息测试用例通过", te='张红彦')

    def test_draw_Course(self,courseId,get_h5_token):
        r = draw_Course(courseId,get_h5_token)
        assert_equal("训练营", r['content']['allCoursePurchasedRecord'][0]['title'], "有训练营课程", te='张红彦')


# def test_dake_no_class(dake_no_class):
#     r = no_class_dacourse()
#     assert_equal("联系课程顾问加入班级", r['content']['allCoursePurchasedRecord'][0]['bigCourseRecordList'][0]['prepayTip'],
#                  "暂未进班", te='张红彦')
#     assert_equal("训练营", r['content']['allCoursePurchasedRecord'][0]['title'], "有训练营课程", te='张红彦')



