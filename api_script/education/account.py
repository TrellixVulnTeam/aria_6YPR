# coding:utf-8
# @Time  : 2020/6/3 19:26
# @Author: Sunnyzhang
# Description:
from api_script.entry.account.passport import password_login
from utils.util import  get_requests,get_edu_app_header



'''def getToken(userToken):
    print("gettoken中的usertoken"+userToken)
    url = 'https://gate.lagou.com/v1/entry/account/h5/getToken'
    # header = get_header(url="https://kaiwu.lagou.com/distribution/appCenter.html")
    header = get_edu_app_header(userToken=userToken,DA=False)
    header["appVersion"]="1.2.7.680"
    header["reqVersion"] = "10207"
    header["lgId"] = "862502040661300_1591588692323"
    remark = "获取gate_login_token"
    return get_requests(url=url, headers=header, remark=remark)'''


def getToken(userToken):
    print("gettoken中的usertoken"+userToken)
    url = 'https://gate.lagou.com/v1/entry/account/h5/getToken'
    # header = get_header(url="https://kaiwu.lagou.com/distribution/appCenter.html")
    header = get_edu_app_header(userToken=userToken,DA=False)
    header["appVersion"]="1.3.0"
    header["reqVersion"] = "10300"
    header["lgId"] = "269D6E0E-0F60-41DD-9518-6BAF4AF862D3_1593075931"
    remark = "获取gate_login_token"
    return get_requests(url=url, headers=header, remark=remark)

