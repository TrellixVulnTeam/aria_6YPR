# coding:utf-8
# @Time  : 2019-02-15 15:32
# @Author: Xiawang
from flask import request
from flask_restful import Resource, reqparse

from api_script.batch.B_postposition import post_position
from utils.util import login


class B_Post_Position(Resource):

	def post(self):
		"""发布职位

		:args
		{
			"countrycode": "00852",  // string, 用户手机号的归属区号
			"username": "20181205",  // string, 用户手机号
			"sum": "1"               // int, 发布职位总数
		}

		:return
			{
				"state": 1,    // int, 1表示成功, 400表示失败
				"message": "发布职位1个, 其中1个成功",
				"content": [{           // 发布成功的职位信息
					"position_name": "金融产品经理",
					"parentPositionId": 1788012,
					"positionId": 13846665
				}],
				"failinfo": [     // 发布失败的职位信息
					null
				]
			}
		"""

		j = 0
		successlist = []
		faillist = [None]
		data = {}
		parser = reqparse.RequestParser()
		parser.add_argument('countrycode', type=str, help="请输入用户手机号的归属区号", required=True)
		parser.add_argument('username', type=str, help="请输入用户的手机号", required=True)
		parser.add_argument('sum', type=int, help="请输入发布职位的数量", required=True)
		args = parser.parse_args()
		login_res = login(args['countrycode'], args['username'])
		if login_res['state'] != 1:
			return {"message": login_res['message']}
		result = post_position(args['sum'])

		state = 0
		for i in result:
			if i['state'] == 1:
				j += 1
				data["position_name"] = i['content']['data']['onlinehunting_position_name']
				data["parentPositionId"] = i['content']['data']['parentPositionInfo']['parentPositionId']
				data["positionId"] = i['content']['data']['parentPositionInfo']['positionChannelInfoList'][0][
					'positionId']
				successlist.append(data)
				data = {}
				state = 1
			else:
				data['state'] = i['state']
				data['message'] = i['message']
				faillist.append(data)
				data = {}
				state = 400

		return {"state": state, "message": "发布职位" + str(args['sum']) + "个, 其中" + str(j) + "个成功", "content": successlist,
		        "errors": faillist}
