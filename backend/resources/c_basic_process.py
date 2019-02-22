# coding:utf-8
# @Time  : 2019-02-15 15:52
# @Author: Xiawang
from flask import request
from flask_restful import Resource, reqparse

from api_script.batch.C_registe_resume import registe_c


class C_Basic_Process(Resource):

	def post(self):
		'''C端注册并生成简历
		args:
		{
			"phone": "20080512",    // string, C端注册用户的手机号
			"countryCode": "00852", // string, C端注册用户的手机号的地区编号
			"userIdentity": 1,    // int, 1学生, 2非学生
			"sum": 1        // int, 构造C端账号的数量
		}


		:return:
		{
		    "state": 1,        // int, 1表示成功, 400表示失败
		    "message": "注册用户2个, 其中注册成功2个, 注册失败0个",
		    "data": [       // 注册成功的手机号
		        20080520,
		        20080521
		    ],
		    "errors": [],   // 注册失败的手机号
		    "detail": []    // 注册失败的详细信息
		}
		'''
		parser = reqparse.RequestParser()
		parser.add_argument('countryCode', type=str, help="请输入注册用户手机号的归属区号", required=True)
		parser.add_argument('phone', type=str, help="请输入注册用户的手机号", required=True)
		parser.add_argument('sum', type=int, help="请输入注册C端用户的数量", required=True)
		parser.add_argument('userIdentity', type=int, help="请输入注册C端用户的类型, 1学生、2非学生", required=True)
		args = parser.parse_args()
		phone = int(args['phone'])
		a = 0
		c_list = []
		e_list = []
		result_list = []
		state = 0
		for i in range(args['sum']):
			a += 1
			r = registe_c(phone, args['countryCode'], args['userIdentity'])
			if len(r) == 8:
				[r1, r2, r3, r4, r5, r6, r7, r8] = r
				if r1['state'] == 1:
					if r2['success'] == r3['success'] == r4['success'] == r5['success'] == r6['success'] == r7[
						'success'] == r8['success']:
						state = 1
						c_list.append(phone)
				else:
					state = 1
					e_list.append(phone)
			elif len(r) == 7:
				[r1, r2, r4, r5, r6, r7, r8] = r
				if r1['state'] == 1:
					if r1['state'] == 1 and r2['success'] == r4['success'] == r5['success'] == r6['success'] == r7[
						'success'] == r8['success']:
						state = 1
						c_list.append(phone)
				else:
					state = 1
					e_list.append(phone)
			else:
				state = 400
				info = {"注册用户": r1['message'], "基本信息": r2['msg'], "工作经历": r3['msg'], "教育经历": r4['msg'],
				        "个人名片": r5['msg'], "求职意向": r6['msg'], "完善信息": r8['msg']}
				result_list.append(info)
			phone += a
		return {'state': state,
		        "message": "注册用户" + str(args['sum']) + "个, 其中注册成功" + str(len(c_list)) + "个, 注册失败" + str(len(e_list)) + "个",
		        "data": c_list, "errors": e_list, "detail": result_list}
