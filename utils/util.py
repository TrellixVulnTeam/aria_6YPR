# coding:utf-8
import os
import time
import zipfile
from datetime import datetime
import datetime
from json import JSONDecodeError
from urllib.parse import urlparse

import pysnooper
import requests
import re
from requests import RequestException
import json
import logging

logging.getLogger().setLevel(logging.ERROR)

requests.packages.urllib3.disable_warnings()
session = requests.session()

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
app_header = {
    'User-Agent': '%E6%8B%89%E5%8B%BE%E6%8B%9B%E8%81%98/7988 CFNetwork/978.0.7 Darwin/18.5.0'
}

count = 0


# 获取页面的token和code
def get_code_token(url, referer=False, ip_port=None):
    global count
    try:
        token_values, code_values = 0, None
        if ip_port is None:
            code = session.get(url=url, headers=header, verify=False, timeout=60)
        else:
            ip_port_url = domain_convert_ip_port(url=url, ip_port=ip_port)
            code = session.get(url=ip_port_url, headers=header, verify=False, timeout=60)
            with open('/home/test/1.log', 'w') as f:
                f.write(code.text)
        token_values = re.findall("X_Anti_Forge_Token = '(.*?)'", code.text, re.S)[0]
        code_values = re.findall("X_Anti_Forge_Code = '(.*?)'", code.text, re.S)[0]
        if referer == False:
            headers = {"X-Anit-Forge-Code": code_values, "X-Anit-Forge-Token": token_values,
                       'Referer': url,
                       "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3615.0 Safari/537.36"}
        else:
            headers = {"X-Anit-Forge-Code": code_values, "X-Anit-Forge-Token": token_values,
                       'referer': 'www.lagou.com',
                       "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3615.0 Safari/537.36"}
        if token_values != '' and code_values != '':
            return headers
        else:
            if count < 1:
                count = count + 1
                return get_code_token(url=url)
            else:
                return headers
    except (RequestException, IndexError):
        return get_code_token(url=url)


def get_code_token_new(url):
    global count
    try:
        token_values, code_values = 0, None
        code = session.get(url=url, headers=header, verify=False, timeout=60)
        token_values = re.findall("X_Anti_Forge_Token = '(.*?)'", code.text, re.S)[0]
        code_values = re.findall("X_Anti_Forge_Code = '(.*?)'", code.text, re.S)[0]
        headers = {"Content-Type": "application/json", "X-Anit-Forge-Code": code_values,
                   "X-Anit-Forge-Token": token_values,
                   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3615.0 Safari/537.36"}
        if token_values != '' and code_values != '':
            return headers
        else:
            if count < 1:
                count = count + 1
                return get_code_token(url=url)
            else:
                return headers
    except (RequestException, IndexError):
        return get_code_token(url=url)


def form_post(url, remark, data=None, files=None, headers={}, allow_redirects=True, ip_port=None):
    """
    form表单传参的post请求
    :param url: 请求url
    :param remark: str, 备注
    :param data: dict, 请求数据
    :param headers: dict, 请求header
    :return: json格式化的响应结果
    """
    global count
    try:
        if not data is None:
            headers = {**header, **headers, **{'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}}
        else:
            headers = {**header, **headers}
        # cookies = dict(X_HTTP_TOKEN='07488fa454ce922a578040585170f3c4f12e21b679')
        if ip_port is None:
            response = session.post(url=url, data=data, files=files, headers=headers, verify=False,
                                    timeout=60,
                                    allow_redirects=allow_redirects)
        else:
            ip_port_url = domain_convert_ip_port(url=url, ip_port=ip_port)
            response = session.post(url=ip_port_url, data=data, files=files, headers=headers, verify=False,
                                    timeout=60,
                                    allow_redirects=allow_redirects)
        pard_id = response.headers.get('Pard-Id', 0)
        status_code = response.status_code
        if 200 <= status_code <= 302:
            response_json = response.json()
            if response_json.get('state', 0) == 1 or response_json.get('success', False):
                logging.info(msg='该接口URL {} ,备注 {} 执行成功\n'.format(url, remark))
                return response_json
            else:
                if count < 1:
                    count = count + 1
                    logging.error(msg='该接口URL {} , 备注: {} , 响应内容: {} 断言失败, 在重试\n'.format(url, remark, response_json))
                    return form_post(url=url, headers=headers, remark=remark, data=data)
                else:
                    logging.error(msg='该接口URL {} , 备注: {},  响应内容: {} 请求成功, 但断言错误\n'.format(url, remark, response_json))
                    return response_json
        else:
            if count < 1:
                count = count + 1
                logging.error(msg='该接口URL {} , 备注: {} , 响应内容: {} 断言失败, 在重试\n'.format(url, remark, response.text))
                return form_post(url=url, headers=headers, remark=remark, data=data)
            else:
                return judging_other_abnormal_conditions(status_code, url, remark, pard_id)
    except RequestException:
        logging.error(msg="该接口URL {} , 备注 {} 请求异常, 请检查接口服务并重试一次\n".format(url, remark))
        return {'content': '请求异常(requests捕获的异常)', 'url': url, 'remark': remark}
    except JSONDecodeError:
        logging.error(msg="该接口URL {} ,备注 {} 报错json解码错误, 请检查接口的响应是否正确的返回并解析\n".format(url, remark))
        return {'content': '响应内容不是期望的json格式', 'url': url, 'remark': remark}


# @pysnooper.snoop()
def json_post(url, remark, data=None, headers={}, app=False, verifystate=True, ip_port=None):
    """
    json传参的post请求
    :param url: 请求url
    :param remark: str, 备注
    :param data: dict, 请求数据
    :param headers: dict, 请求header
    :return: json格式化的响应结果
    """
    global count
    if verifystate == False:
        count = 3
    if app == False:
        headers = {**header, **headers, **{'Content-Type': 'application/json;charset=UTF-8'}}
    try:
        if ip_port is None:
            response = session.post(url=url, json=data, headers=headers, verify=False, timeout=60)
        else:
            ip_port_url = domain_convert_ip_port(url=url, ip_port=ip_port)
            response = session.post(url=ip_port_url, json=data, headers=headers, verify=False,
                                    timeout=60)
        pard_id = response.headers.get('Pard-Id', 0)
        status_code = response.status_code
        if 200 <= status_code <= 302:
            response_json = response.json()
            if response_json.get('state', 0) == 1 or response_json.get('success', False):
                logging.info(msg='该接口URL {} ,备注 {} 执行成功\n'.format(url, remark))
                return response_json
            else:
                if count < 1:
                    count = count + 1
                    logging.error(msg='该接口URL {} , 备注: {} , 响应内容: {} 断言失败, 在重试\n'.format(url, remark, response_json))
                    return json_post(url=url, headers=headers, remark=remark, data=data)
                else:
                    logging.error(msg='该接口URL {} , 备注 {}, 响应内容: {} 请求成功, 但断言错误\n'.format(url, remark, response_json))
                    return response_json
        else:
            if count < 1:
                count = count + 1
                logging.error(msg='该接口URL {} , 备注: {} , 响应内容: {} 断言失败, 在重试\n'.format(url, remark, response.text))
                return json_post(url=url, headers=headers, remark=remark, data=data)
            else:
                return judging_other_abnormal_conditions(status_code, url, remark, pard_id)
    except RequestException as e:
        print(e)
        logging.error(msg="该接口URL {} , 备注 {} 请求异常, 请检查接口服务并重试一次\n".format(url, remark))
        return {'content': '请求执行错误', 'url': url, 'remark': remark}
    except JSONDecodeError:
        logging.error(msg="该接口URL {} ,备注 {} 报错json解码错误, 请检查接口的响应是否正确的返回并解析\n".format(url, remark))
        return {'content': '响应内容不是期望的json格式', 'url': url, 'remark': remark}


def get_requests(url, data=None, headers={}, remark=None, ip_port=None):
    """
    get请求
    :param url: str, 接口地址
    :param remark: str, 备注
    :param headers: dict, requests header
    :return: object, 响应对象
    """
    headers = {**header, **headers, **{'Content-Type': 'charset=UTF-8'}}
    global count
    try:

        if ip_port is None:
            response = session.get(url=url, params=data, headers=headers, verify=False, timeout=60)
        else:
            ip_port_url = domain_convert_ip_port(url=url, ip_port=ip_port)
            response = session.get(url=ip_port_url, params=data, headers=headers, verify=False, timeout=60)
        status_code = response.status_code
        pard_id = response.headers.get('Pard-Id', 0)
        if 200 <= status_code <= 302:
            try:
                response_json = response.json()
                if response_json.get('state', 0) == 1 or response_json.get('success', False):
                    logging.info(msg='该接口URL {} ,备注 {} 执行成功\n'.format(url, remark))
                    return response
                else:
                    if count < 1:
                        count = count + 1
                        logging.error(
                            msg='该接口URL {} , 备注: {} , 响应内容: {} 断言失败, 在重试\n'.format(url, remark, response_json))
                        return get_requests(url=url, data=data, headers=headers, remark=remark)
                    else:
                        logging.error(
                            msg='该接口URL {} , 备注 {}, 响应内容: {} 请求成功, 但断言错误\n'.format(url, remark, response_json))
                        return response
            except JSONDecodeError:
                return response
        else:
            if count < 1:
                count += 1
                logging.error(
                    msg='该接口URL {} , 备注: {} , 响应内容: {} 断言失败, 在重试\n'.format(url, remark, response.text))
                return get_requests(url, data=data, headers=headers, remark=remark)
            else:
                return judging_other_abnormal_conditions(status_code, url, remark, pard_id)
    except RequestException:
        logging.error(msg="该接口URL {} , 备注 {} 请求异常, 请检查接口服务并重试一次\n".format(url, remark))
        return {'content': '请求执行错误', 'url': url, 'remark': remark}
    except JSONDecodeError:
        logging.error(msg="该接口URL {} ,备注 {} 报错json解码错误, 请检查接口的响应是否正确的返回并解析\n".format(url, remark))
        return {'content': '响应内容不是期望的json格式', 'url': url, 'remark': remark}


# get请求---获取header
def get_header(url, headers={}, allow_redirects=True, ip_port=None):
    headers = {**header, **headers}
    try:
        if ip_port is None:
            response = session.get(url=url, headers=headers, verify=False, timeout=60, allow_redirects=allow_redirects)
        else:
            ip_port_url = domain_convert_ip_port(url=url, ip_port=ip_port)
            response = session.get(url=ip_port_url, headers=headers, verify=False, timeout=60,
                                   allow_redirects=allow_redirects)
        if response.status_code == 200:
            return response.request.headers
    except RequestException as e:
        return {"errors": str(e)}


# 企业微信报警
def wxsend(username, content):
    s = {'userids': username, 'msgtype': 'text', 'content': content}
    params = json.dumps(s)
    try:
        content = requests.post('http://api.oss.lagou.com/v2/send/wechat/', data=params, timeout=3)
        if content.status_code != 200:
            raise IOError("exception")
    except  Exception as e:
        raise IOError("exception")


def login(countryCode, username):
    '''
    从www.lagou.com登录，验证码登录
    :param countryCode: str, 地区编号
    :param username: str, 用户名
    '''
    session.cookies.clear()
    login_url = 'https://passport.lagou.com/login/login.json'
    login_data = {'isValidate': 'true', 'username': username, 'phoneVerificationCode': '049281',
                  'countryCode': countryCode, 'challenge': 111}
    referer_login_html = 'https://www.lagou.com/frontLogin.do'
    login_header = get_code_token(referer_login_html)
    remark = str(username) + "在登录拉勾"
    r = form_post(url=login_url, data=login_data, headers=login_header, remark=remark)
    if r['message'] == "操作成功":
        logging.info("用户名: " + str(username) + " 登录成功")
    return r


def login_home(username, password):
    '''
    从home.lagou.com登录，密码登录
    :param username: str, 用户名
    :param password: str, 密码
    :param remark: str, 备注
    '''
    session.cookies.clear()
    referer_login_home_url = "https://home.lagou.com/"
    login_url = 'https://passport.lagou.com/login/login.json'
    login_data = {'isValidate': 'true', 'username': username, 'password': password}
    login_home_header = get_code_token(referer_login_home_url)
    remark = "用户 " + str(username) + " 在登录拉勾home后台"
    r = form_post(url=login_url, data=login_data, headers=login_home_header, remark=remark)
    get_requests(url='https://passport.lagou.com/grantServiceTicket/grant.html')
    if r['message'] == "操作成功":
        logging.info("用户名: " + str(username) + " 登录成功")
    return r


def login_home_code(countryCode, username):
    '''
    从www.lagou.com登录，验证码登录
    :param countryCode: str, 地区编号
    :param username: str, 用户名
    '''
    session.cookies.clear()
    referer_login_home_url = "https://home.lagou.com/"
    login_url = 'https://passport.lagou.com/login/login.json'
    login_data = {'isValidate': 'true', 'username': username, 'phoneVerificationCode': '049281',
                  'countryCode': countryCode, 'challenge': 111}
    login_header = get_code_token(referer_login_home_url)
    remark = str(username) + "在登录拉勾"
    r = form_post(url=login_url, data=login_data, headers=login_header, remark=remark)
    if r['message'] == "操作成功":
        logging.info("用户名: " + str(username) + " 登录成功")
    return r


def assert_equal(expectvalue, actualvalue, success_message, fail_message=None):
    '''
    断言两个值是否相等, 并对结果打印日志
    :param expectvalue: 期望结果
    :param actualvalue: 实际结果
    :param success_message: str, 断言成功打印的日志
    :param fail_message:str, 断言失败打印的日志
    '''
    assert expectvalue == actualvalue
    if expectvalue == actualvalue:
        logging.info(success_message)
        return 1
    else:
        logging.error(fail_message)
        return 0


def assert_not_equal(expectvalue, actualvalue, success_message, fail_message=None):
    '''
    断言两个值是否相等, 并对结果打印日志
    :param expectvalue: 期望结果
    :param actualvalue: 实际结果
    :param success_message: str, 断言成功打印的日志
    :param fail_message:str, 断言失败打印的日志
    '''
    assert expectvalue != actualvalue
    if expectvalue != actualvalue:
        logging.info(success_message)
    else:
        logging.error(fail_message)


def assert_in(expect_value, actual_value, success_message, fail_message=None):
    '''
    断言两个值是否相等, 并对结果打印日志
    :param expectvalue: 期望结果
    :param actualvalue: 实际结果
    :param success_message: str, 断言成功打印的日志
    :param fail_message:str, 断言失败打印的日志
    '''
    try:
        assert expect_value in actual_value
        logging.info(success_message)
    except AssertionError:
        logging.info(fail_message)
        raise AssertionError


def assert_not_in(expect_value, actual_value, success_message, fail_message=None):
    '''
    断言两个值是否相等, 并对结果打印日志
    :param expectvalue: 期望结果
    :param actualvalue: 实际结果
    :param success_message: str, 断言成功打印的日志
    :param fail_message:str, 断言失败打印的日志
    '''
    try:
        assert expect_value not in actual_value
        logging.info(success_message)
    except AssertionError:
        logging.info(fail_message)
        raise AssertionError


# 获取url的html源码
def gethtml(url):
    '''

    :param url:
    :return:
    '''
    html = session.get(url)
    return html.text


def wait(time):
    '''
    设置等待时间
    :param time:
    :return:
    '''


def get_app_header(userId, reqVersion=80201):
    header = {"Accept": "application/json", "X-L-REQ-HEADER": {"deviceType": 10, "reqVersion": reqVersion},
              "X-L-USER-ID": str(userId),
              "X-L-DA-HEADER": "da5439aadaf04ade94a214d730b990d83ec71d3e9f274002951143c843badffbc543b213dfe84e21a37bb782dd9bbca4be8d947ead7041f79d336cb1217127d15"}
    header["X-L-REQ-HEADER"] = json.dumps(header["X-L-REQ-HEADER"])
    return header


def get_app_header1(userId):
    header = {"Content-Type": "application/json", "X-L-REQ-HEADER": {"deviceType": 10},
              "X-L-USER-ID": str(userId),
              "X-L-DA-HEADER": "da5439aadaf04ade94a214d730b990d83ec71d3e9f274002951143c843badffbc543b213dfe84e21a37bb782dd9bbca4be8d947ead7041f79d336cb1217127d15"}
    header["X-L-REQ-HEADER"] = json.dumps(header["X-L-REQ-HEADER"])
    return header


def get_app_header_new(userId, X_L_REQ_HEADER={}):
    app_header = {"deviceType": 10}
    X_L_REQ_HEADER = {**app_header, **X_L_REQ_HEADER}
    header = {"Accept": "application/json", "X-L-REQ-HEADER": X_L_REQ_HEADER,
              "X-L-USER-ID": str(userId),
              "User-Agent": "%E6%8B%89%E5%8B%BE%E6%8B%9B%E8%81%98/7945 CFNetwork/978.0.7 Darwin/18.5.0",
              "X-L-DA-HEADER": "da5439aadaf04ade94a214d730b990d83ec71d3e9f274002951143c843badffbc543b213dfe84e21a37bb782dd9bbca4be8d947ead7041f79d336cb1217127d15"}
    header["X-L-REQ-HEADER"] = json.dumps(header["X-L-REQ-HEADER"])
    return header


def json_put(url, remark, data=None, headers={}, ip_port=None):
    """
    json传参的put请求
    :param url: 请求url
    :param remark: str, 备注
    :param data: dict, 请求数据
    :param headers: dict, 请求header
    :return: json格式化的响应结果
    """
    global count
    try:
        headers = {**headers, **header, **{'Content-Type': 'application/json;charset=UTF-8'}}
        if ip_port is None:
            response = session.put(url=url, json=data, headers=headers, verify=False, timeout=60)
        else:
            ip_port_url = domain_convert_ip_port(url=url, ip_port=ip_port)
            response = session.put(url=ip_port_url, json=data, headers=headers, verify=False, timeout=60)

        pard_id = response.headers.get('Pard-Id', 0)
        status_code = response.status_code
        if 200 <= status_code <= 400:
            response_json = response.json()
            if response_json.get('state', 0) == 1 or response_json.get('success', False):
                logging.info(msg='该接口URL {} ,备注 {} 执行成功\n'.format(url, remark))
                return response_json
            else:
                if count < 1:
                    count = count + 1
                    logging.error(msg='该接口URL {} , 备注: {} , 响应内容: {} 断言失败, 在重试\n'.format(url, remark, response_json))
                    return json_put(url=url, headers=headers, remark=remark, data=data)
                else:
                    logging.error(msg='该接口URL {} , 备注 {}, 响应内容: {} 请求成功, 但断言错误\n'.format(url, remark, response_json))
                    return response_json
        else:
            if count < 1:
                count = count + 1
                logging.error(msg='该接口URL {} , 备注: {} , 响应内容: {} 断言失败, 在重试\n'.format(url, remark, response.text))
                return json_put(url=url, headers=headers, remark=remark, data=data)
            else:
                return judging_other_abnormal_conditions(status_code, url, remark, pard_id)
    except RequestException as e:
        logging.error(msg="该接口URL {} , 备注 {} 请求异常, 请检查接口服务并重试一次\n该异常为{}".format(url, remark, e))
        return {'content': '请求执行错误', 'url': url, 'remark': remark}
    except JSONDecodeError:
        logging.error(msg="该接口URL {} ,备注 {} 报错json解码错误, 请检查接口的响应是否正确的返回并解析\n".format(url, remark))
        return {'content': '响应内容不是期望的json格式', 'url': url, 'remark': remark}


def put_requests(url, headers={}, remark=None, ip_port=None):
    """
    put请求
    :param url: str, 接口地址
    :param remark: str, 备注
    :param headers: dict, requests header
    :return: object, 响应对象
    """
    global count
    try:
        if ip_port is None:
            response = session.put(url=url, headers=headers, verify=False, timeout=60)
        else:
            ip_port_url = domain_convert_ip_port(url=url, ip_port=ip_port)
            response = session.put(url=ip_port_url, headers=headers, verify=False, timeout=60)
        pard_id = response.headers.get('Pard-Id', 0)
        status_code = response.status_code
        if 200 <= status_code <= 400:
            response_json = response.json()
            if response_json.get('state', 0) == 1 or response_json.get('success', False):
                logging.info(msg='该接口URL {} ,备注 {} 执行成功\n'.format(url, remark))
                return response_json
            else:
                if count < 1:
                    count = count + 1
                    logging.error(msg='该接口URL {} , 备注: {} , 响应内容: {} 断言失败, 在重试\n'.format(url, remark, response_json))
                    return put_requests(url=url, headers=headers, remark=remark)
                else:
                    logging.error(msg='该接口URL {} , 备注 {}, 响应内容: {} 请求成功, 但断言错误\n'.format(url, remark, response_json))
                    return response_json
        else:
            if count < 1:
                count = count + 1
                logging.error(msg='该接口URL {} , 备注: {} , 响应内容: {} 断言失败, 在重试\n'.format(url, remark, response.text))
                return put_requests(url=url, headers=headers, remark=remark)
            else:
                return judging_other_abnormal_conditions(status_code, url, remark, pard_id)
    except RequestException:
        logging.error(msg="该接口URL {} , 备注 {} 请求异常, 请检查接口服务并重试一次\n".format(url, remark))
        return {'content': '请求执行错误', 'url': url, 'remark': remark}
    except JSONDecodeError:
        logging.error(msg="该接口URL {} ,备注 {} 报错json解码错误, 请检查接口的响应是否正确的返回并解析\n".format(url, remark))
        return {'content': '响应内容不是期望的json格式', 'url': url, 'remark': remark}


def delete_requests(url, headers={}, remark=None, ip_port=None):
    """
    put请求
    :param url: str, 接口地址
    :param remark: str, 备注
    :param headers: dict, requests header
    :return: object, 响应对象
    """
    global count
    try:
        if ip_port is None:
            response = session.delete(url=url, headers=headers, verify=False, timeout=60)
        else:
            ip_port_url = domain_convert_ip_port(url=url, ip_port=ip_port)
            response = session.delete(url=ip_port_url, headers=headers, verify=False, timeout=60)
        pard_id = response.headers.get('Pard-Id', 0)
        status_code = response.status_code
        if 200 <= status_code <= 302:
            response_json = response.json()
            if response_json.get('state', 0) == 1 or response_json.get('success', False):
                logging.info(msg='该接口URL {} ,备注 {} 执行成功\n'.format(url, remark))
                return response_json
            else:
                if count < 1:
                    count = count + 1
                    logging.error(msg='该接口URL {} , 备注: {} , 响应内容: {} 断言失败, 在重试\n'.format(url, remark, response_json))
                    return delete_requests(url=url, headers=headers, remark=remark)
                else:
                    logging.error(msg='该接口URL {} , 备注 {}, 响应内容: {} 请求成功, 但断言错误\n'.format(url, remark, response_json))
                    return response_json
        else:
            if count < 1:
                count = count + 1
                logging.error(msg='该接口URL {} , 备注: {} , 响应内容: {} 断言失败, 在重试\n'.format(url, remark, response.text))
                return delete_requests(url=url, headers=headers, remark=remark)
            else:
                return judging_other_abnormal_conditions(status_code, url, remark, pard_id)
    except RequestException:
        logging.error(msg="该接口URL {} , 备注 {} 请求异常, 请检查接口服务并重试一次\n".format(url, remark))
        return {'content': '请求执行错误', 'url': url, 'remark': remark}
    except JSONDecodeError:
        logging.error(msg="该接口URL {} ,备注 {} 报错json解码错误, 请检查接口的响应是否正确的返回并解析\n".format(url, remark))
        return {'content': '响应内容不是期望的json格式', 'url': url, 'remark': remark}


def dfs_get_zip_file(input_path, result):
    #
    files = os.listdir(input_path)
    for file in files:
        if os.path.isdir(input_path + '/' + file):
            dfs_get_zip_file(input_path + '/' + file, result)
        else:
            result.append(input_path + '/' + file)


def zip_path(input_path, output_path, output_name):
    f = zipfile.ZipFile(output_path + '/' + output_name, 'w', zipfile.ZIP_DEFLATED)
    filelists = []
    dfs_get_zip_file(input_path, filelists)
    for file in filelists:
        f.write(file)
    f.close()
    file_Path = os.path.abspath(os.path.join(os.getcwd(), ".."))
    zip_file_Path = os.path.join(file_Path, output_name)
    return zip_file_Path


def judging_other_abnormal_conditions(status_code, url, remark, pard_id=None):
    if bool(pard_id):
        call_chain = ' 其调用链:http://oss.pard.inter.lagou.com/#/traDetail?traceId={}'.format(pard_id)
    else:
        call_chain = ''

    if status_code == 500:
        logging.error(msg="该接口URL {} , 备注 {} 报错500, 请检查业务服务是否可用,{}\n".format(url, remark, call_chain))
        return {'content': '报错500, 服务端错误', 'url': url, 'remark': remark + call_chain}
    elif status_code == 415:
        logging.error(msg="该接口URL {} 备注 {} 报错415, 请检查接口的请求方法是否正确\n".format(url, remark))
        return {'content': '报错415, 接口请求方法不可用', 'url': url, 'remark': remark}
    elif status_code == 404:
        logging.error(msg="该接口URL {} , 备注 {} 报错404, 请检查接口地址是否正确及业务服务是否可用,{}\n".format(url, remark, call_chain))
        return {'content': '报错404, 接口地址不可用', 'url': url, 'remark': remark + call_chain}
    elif status_code == 401:
        logging.error(msg="该接口URL {} , 备注 {} 报错401 请检查接口的用户认证是否有效\n".format(url, remark))
        return {'content': '报错401, 接口的用户认证失效', 'url': url, 'remark': remark}
    elif status_code == 400:
        logging.error(msg="该接口URL {} , 备注 {} 报错400 请检查接口的传参是否有效\n".format(url, remark))
        return {'content': '报错400, 接口的传参有误', 'url': url, 'remark': remark}
    elif status_code == 502:
        logging.error(msg="该接口URL {} , 备注 {} 报错502, 请检查业务服务是否可用,{}\n".format(url, remark, call_chain))
        return {'content': '报错502, 业务服务不可用', 'url': url, 'remark': remark + call_chain}
    else:
        return {'content': '报错{}, 请检查业务服务是否正常, {}'.format(status_code, call_chain), 'url': url, 'remark': remark}


f = 0


def get_verify_code_list(countryCode, phone):
    if countryCode == '0086':
        countryCode = ''
    url = 'https://home.lagou.com/msc/message/page'
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    data = {"commId": countryCode + phone, "startTime": str(yesterday) + "T16:00:00.000Z", 'templateId': '749',
            "page": 1, "count": 10}
    r = json_post(url=url, data=data, headers={'X-L-REQ-HEADER': json.dumps({"deviceType": 1})}, remark="获取验证码列表")
    try:
        if r['content']['totalCount'] == 0:
            return 0, None, None
        else:
            return r['content']['totalCount'], r['content']['result'][0]['msgId'], r['content']['result'][0][
                'createTime']
    except IndexError:
        return 0, None, None


def verify_code_message(countryCode, phone, flag_num=0):
    login_home('betty@lagou.com', '00f453dfec0f2806db5cfabe3ea94a35')
    import time
    for i in range(10):
        time.sleep(12)
        total_count, id, createTime = get_verify_code_list(countryCode, phone)
        if total_count > flag_num:
            verify_code = get_verify_code(id, createTime)
            if verify_code:
                return verify_code


def get_verify_code(id, createTime):
    url = 'https://home.lagou.com/msc/message/view'
    data = {"createTime": createTime, "msgId": id}
    r = json_post(url=url, data=data, headers={'X-L-REQ-HEADER': json.dumps({"deviceType": 1})}, remark="获取验证码")
    try:
        int(r['content']['content'][3:9])
    except ValueError:
        return None
    return r['content']['content'][3:9]


# @pysnooper.snoop()
def get_verify_code_message_len(countryCode, phone):
    login_home('betty@lagou.com', '00f453dfec0f2806db5cfabe3ea94a35')
    if countryCode == '0086':
        countryCode = ''
    time.sleep(2)
    url = 'https://home.lagou.com/msc/message/page'
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    data = {"commId": countryCode + phone, "startTime": str(yesterday) + "T16:00:00.000Z",
            "page": 1, "count": 10, 'templateId': '749'}
    r = json_post(url=url, data=data, headers={'X-L-REQ-HEADER': json.dumps({"deviceType": 1})}, remark="获取验证码列表")
    try:
        return r['content']['totalCount']
    except:
        return -1


def app_header_999(userToken=None, DA=True, userId=None):
    header = {"deviceType": '150', "userType": '0', "lgId": "898BCC3F-E662-4761-87E8-845788525443_1532945379",
              "reqVersion": '73100', "appVersion": "7.31.0"}
    if not userToken is None:
        header['userToken'] = userToken

    header = {'X-L-REQ-HEADER': json.dumps(header)}

    header = {**app_header, **header}
    if userId:
        header['X-L-USER-ID'] = str(userId)
    if DA == False:
        return header
    header[
        'X-L-DA-HEADER'] = "da5439aadaf04ade94a214d730b990d83ec71d3e9f274002951143c843badffbc543b213dfe84e21a37bb782dd9bbca4be8d947ead7041f79d336cb1217127d15"
    return header


def login_password(username, password):
    '''
    从www.lagou.com登录，验证码登录
    :param countryCode: str, 地区编号
    :param username: str, 用户名
    '''
    session.cookies.clear()
    # login_url = 'https://passport.lagou.com/login/login.json?isValidate=true&username={}&password={}&request_form_verifyCode=&_={}'.format()
    login_url = 'https://passport.lagou.com/login/login.json'
    login_data = {'isValidate': 'true', 'username': username,
                  'password': password}
    referer_login_html = 'https://passport.lagou.com/login/login.html'
    login_header = get_code_token(referer_login_html)
    remark = str(username) + "在登录拉勾"
    r = form_post(url=login_url, data=login_data, headers=login_header, remark=remark)
    if r['message'] == "操作成功":
        logging.info("用户名: " + str(username) + " 登录成功")
    return r


def login_verifyCode(countryCode, phone, verifyCode):
    '''
    从www.lagou.com登录，验证码登录
    :param countryCode: str, 地区编号
    :param username: str, 用户名
    '''
    session.cookies.clear()
    login_url = 'https://passport.lagou.com/login/login.json'
    login_data = {'isValidate': 'true', 'username': phone,
                  'phoneVerificationCode': verifyCode, 'countryCode': countryCode}
    referer_login_html = 'https://passport.lagou.com/login/login.html'
    login_header = get_code_token(referer_login_html)
    remark = str(phone) + "在登录拉勾"
    r = form_post(url=login_url, data=login_data, headers=login_header, remark=remark)
    if r['message'] == "操作成功":
        logging.info("用户名: " + str(phone) + " 登录成功")
    return r


def pc_send_register_verifyCode(countryCode, phone):
    session.cookies.clear()
    url = 'https://passport.lagou.com/register/getPhoneVerificationCode.json'
    header = get_header(url='https://passport.lagou.com/register/register.html')
    send_data = {'countryCode': countryCode, 'phone': phone, 'type': 0, 'request_form_verifyCode': '', '_': str(int(
        time.time())) + '000'}
    return form_post(url=url, headers=header, data=send_data, remark='发送验证码')['state']


def pc_send_login_verifyCode(countryCode, phone):
    url = 'https://passport.lagou.com/login/sendLoginVerifyCode.json'
    header = get_header(url='https://passport.lagou.com/login/login.html')
    send_data = {'countryCode': countryCode, 'phone': phone, 'type': 0, 'request_form_verifyCode': '', '_': str(int(
        time.time())) + '000'}
    return form_post(url=url, headers=header, data=send_data, remark='发送验证码')['state']


def user_register_lagou(countryCode, phone, verify_code):
    b_register_url = 'https://passport.lagou.com/register/register.html?from=b'
    register_url = "https://passport.lagou.com/register/register.json"
    register_data = {"isValidate": "true", "phone": phone, "phoneVerificationCode": verify_code, "challenge": 111,
                     "type": 1, "countryCode": countryCode}
    register_header = get_code_token(b_register_url)
    remark = "验证B端注册"
    return form_post(url=register_url, data=register_data, headers=register_header, remark=remark)


def request_retry(count, request_func, judging_func=None, response_text=None):
    if count < 1:
        count += 1
        return request_func
    elif not response_text is None:
        return response_text
    else:
        judging_func


def domain_convert_ip_port(url, ip_port):
    parsed = urlparse(url)
    if 'gate.lagou.com' == parsed.hostname:
        gate_lagou_com_rule = {'entry': 'gate.lagou.com/v1/entry', 'neirong': 'gate.lagou.com/v1/neirong',
                               'zhaopin': 'gate.lagou.com/v1/zhaopin'}
        domain, verison, module = re.findall(r"https://(.+?)/(.+?)/(.+?)/", url)[0]
        return url.replace('https', 'http').replace(gate_lagou_com_rule.get(module), ip_port)
    return url.replace('https', 'http').replace(parsed.hostname, ip_port)


if __name__ == '__main__':
    # r = get_verify_code_message_len('00852', '20180917')
    # pc_send_register_verifyCode("00853", "26026626")
    # verify_code = verify_code_message("00853", "26026626")
    # print(verify_code)
    # r = verify_code_message('00852', '20180917')
    # get_verify_code('r23wr23','423423')
    # r1 = get_verify_code_message_len('00852', '20180917')
    # print(r1)
    # print(r1l)
    # login_password('betty@lagou.com', '00f453dfec0f2806db5cfabe3ea94a35')
    # state_code = pc_send_register_verifyCode('00852', 20030105)
    # print(verify_code_message('00852', '20030105', flag_num=1))
    # login_home('betty@lagou.com', '00f453dfec0f2806db5cfabe3ea94a35')
    # get_requests(url='https://passport.lagou.com/grantServiceTicket/grant.html')
    # url = 'https://home.lagou.com/msc/message/page'
    # data = {"commId": "0085220180917", "startTime": "2020-03-30T12:19:52.709Z", "page": 1, "count": 10}
    # r = requests.post(url=url, json=data, verify=False).text

    # url = 'https://home.lagou.com/msg/message-service/index.html'
    # header = get_header(url='http://home.lagou.com/index.html')
    # get_requests(url=url,headers=header,remark='23')
    # r = verify_code_message('00852', '20180917')
    # r = domain_convert_ip_port('https://gate.lagou.com/v1/entry/demo/demo/sdfas', '127.0.0.1:8080')
    # r = domain_convert_ip_port('https://easy.lagou.com/parentPosition/multiChannel/create.json', '10.42.154.224:11170')
    r = get_verify_code_message_len('00852', '20180917')
    print(r)
    # r = verify_code_message('00852', '20180917')
    # print(r)
    # login_home('betty@lagou.com', '00f453dfec0f2806db5cfabe3ea94a35')
    # get_requests(url='https://passport.lagou.com/grantServiceTicket/grant.html')
    # r = get_verify_code_list('00852', '20180917')
    # print(r)
