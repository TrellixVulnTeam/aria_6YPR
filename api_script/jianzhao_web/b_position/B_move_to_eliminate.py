# coding:utf-8
# @Author: Xiawang
from utils.util import form_post,get_code_token, login,get_requests

'''
简历管理-候选人: 从面试移至淘汰
'''

# username = 20181205
# login("00852",username)

# 面试的候选人移动到淘汰
# refer_listofcandidates_url = "https://easy.lagou.com/can/index.htm"
# listofcandidates_header = get_code_token(refer_listofcandidates_url)
# newlist_url = "https://easy.lagou.com/can/new/list.json"
# newlist_data = {"pageNo":0,"stage":"INTERVIEW","can":"true","needQueryAmount":"true","newDeliverTime":0}
# r = form_post(newlist_url, newlist_data,listofcandidates_header)
# positionId = r['content']['rows'][0]['positionId']
# resumeOwnerId = r['content']['rows'][0]['id']
# login('00853','05180001')
def move_to_eliminate(positionId,resumeOwnerId):
    refer_listofcandidates_url = "https://easy.lagou.com/can/index.htm"
    listofcandidates_header = get_code_token(refer_listofcandidates_url)
    url = 'https://easy.lagou.com/settings/template/in_temp.json?positionId='+str(positionId)
    get_requests(url=url,headers=listofcandidates_header)


    obsolete_url = 'https://easy.lagou.com/can/obsolete.json'
    obsolete_data = {"reason":"条件不太匹配","content":"非常荣幸收到您的简历，经过我们评估，认为您与该职位不太合适，无法进入面试阶段。",
                         "resumeId":resumeOwnerId,"needNotice":"true"}
    r = form_post(url=obsolete_url,headers=listofcandidates_header ,data=obsolete_data,remark='淘汰')
    return r
# move_to_eliminate(13844989,1082604611225001984)