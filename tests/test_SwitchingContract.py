# coding:utf-8
# @Author: cloudyyuan

'''
登录home 然后根据版本号更换套餐
'''
from api_script.business.SwitchingContract import lagouPlus
from utils.util import login_home,form_post,get_header
import json
'''
获取当前时间
'''
def test_lagouPlus():
    '''
    终止当前套餐
    新增17套餐
    查看套餐是否正常
    :return:
    '''
    lagouPlus(87)