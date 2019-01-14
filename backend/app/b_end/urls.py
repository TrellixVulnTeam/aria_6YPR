# coding:utf-8
# @Time  : 2019-01-10 10:39
# @Author: Xiawang
from flask import Blueprint
from flask_restful import Api

from backend.app.b_end.api import B_Post_Position, B_Basic_Process, HelloWorld, C_Basic_Process

app_api = Blueprint(name="b_end", import_name=__name__)
restful_api = Api(app_api)

restful_api.add_resource(HelloWorld, "/")
restful_api.add_resource(B_Post_Position, "/postposition")
restful_api.add_resource(B_Basic_Process, "/bbasicprocess")
restful_api.add_resource(C_Basic_Process, "/cbasicprocess")
