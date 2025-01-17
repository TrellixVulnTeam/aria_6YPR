# coding:utf-8
# @Time  : 2019-02-15 15:57
# @Author: Xiawang
import logging
import os
import subprocess

from flask import render_template, make_response
from flask_restful import Resource, reqparse
from utils.analysis_html_report import analysis_html_report
from flask import current_app


class run_Pytest(Resource):
    """执行pytest"""
    business_module = {
        'mainprocess': 'pytest {}/tests/test_mainprocess/ --html=backend/templates/{}_report.html --self-contained-html -s -v',
        'lg-zhaopin-boot': 'pytest {}/tests/test_lg_zhaopin_boot/ --html=backend/templates/{}_report.html --self-contained-html {}',
        'lg-entry-boot': 'pytest {}/tests/test_lg_entry_boot/ --html=backend/templates/{}_report.html --self-contained-html {}',
        'lg-neirong-boot': 'pytest {}/tests/test_lg_neirong_boot/ --html=backend/templates/{}_report.html --self-contained-html {}',
        'open_api_lagou': 'pytest {}/tests/test_open_api_lagou_com/ --html=backend/templates/{}_report.html --self-contained-html'
    }

    def get(self):
        '''获取pytest测试报告
        @@@
        ### 对外接口: 获取pytest测试报告

        ### Author = Xiawang

        ### Request Header
        | 字段 | 值 |
        | ---- | ---- |
        | method | GET |
        | Accept | text/html |


        ### 参数

        | 字段 | 必填 | 类型 | 描述|
        | ---- | ---- | ---- | ---- |
        | module | True | string | 选项值, business, jianzhao_web, zhaopin, all |
        |  |  | string | jianzhao_web，简招web |
        |  |  | string | zhaopin， 招聘业务 |
        |  |  | string | business, 商业业务 |
        |  |  | string | entry_app, app端的入口业务 |
        |  |  | string | neirong_app, app端的内容业务 |
        |  |  | string | all, 全部业务 |


        ### 请求示例--直接在浏览器请求访问
        ```json
        http://127.0.0.1:9004/pytest?module=business

        http://127.0.0.1:9004/pytest?module=jianzhao_web

        http://127.0.0.1:9004/pytest?module=zhaopin
        ```

        ### 返回
         report html

        '''
        parser = reqparse.RequestParser()
        parser.add_argument('module', type=str,
                            required=True)
        args = parser.parse_args()
        headers = {'Content-Type': 'text/html'}
        html = '{}_report.html'.format(args['module'])
        return make_response(render_template(html), 200, headers)

    def post(self):
        '''执行pytest
        @@@
        ### 对外接口: 执行pytest

        ### Author = Xiawang

        ### Request Header
        | 字段 | 值 |
        | ---- | ---- |
        | method | POST |
        | content-type | application/json |


        ### 参数

        | 字段 | 必填 | 类型 | 描述|
        | ---- | ---- | ---- | ---- |
        | module | True | string | 选项值, lg-zhaopin-boot, jianzhao_web, zhaopin, all |
        |  |  | string | jianzhao_web，简招web |
        |  |  | string | zhaopin， 招聘业务 |
        |  |  | string | business, 商业业务 |
        |  |  | string | entry_app, app端的入口业务 |
        |  |  | string | neirong_app, app端的内容业务 |
        |  |  | string | all, 全部业务 |


        ### 请求示例
        ```json
         {
            "module":"business"
         }
        ```


        ### 返回

        | 字段 | 类型 | 描述|
        | ---- | ---- | ---- | ---- |
        | state | int | 1表示成功, 400表示错误 |
        | data | dict | 构造数据的结果 |
        | result | dict | 测试报告信息 |
        | content | string | 报告生成结果 |
        | info | dict | 报告的具体信息 |
        | time | list | 报告的生成时间 |
        | result | list | 测试用例执行的汇总结果 |


        ### 响应示例
        ```json
        {
            "state": 1,
            "content": {
                "result": {
                    "content": "报告生成成功",
                    "info": {
                        "time": [
                            "Report generated on 03-Mar-2019 at 12:13:05 by pytest-html v1.20.0",
                            "13 tests ran in 87.12 seconds. "
                        ],
                        "result": [
                            [
                                "8 passed",
                                "0 skipped",
                                "5 failed",
                                "0 errors",
                                "0 expected failures",
                                "0 unexpected passes"
                            ],
                            null
                        ]
                    }
                }
            }
        }
        ```

        @@@
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('module', type=str,
                            help="请输入正确模块值",
                            required=True)
        parser.add_argument('ip_port', type=str,
                            help="ip:port", default=None
                            )
        args = parser.parse_args()
        current_app.logger.info(f'请求数据:{args}')
        if self.business_module.get(args['module']) is None:
            return {'state': 2, "data": "不支持该业务模块"}

        if args['ip_port']:
            if not (len(args['ip_port'].split('.')) == 4 and len(args['ip_port'].split(':')) == 2):
                return {'state': 3, "data": "ip:port 不正确"}

        state = 1
        project_path = self.switch_project_root_directory()

        cmd_str = self.get_run_pytest_cmd(args['module'], project_path, args['ip_port'])
        ret = subprocess.run(cmd_str, shell=True, timeout=300, stdout=subprocess.PIPE, encoding='utf-8')
        current_app.logger.info(f'本次pytest的returncode执行结果: {ret.returncode}')
        current_app.logger.info(f'py_test执行结果:{ret.stdout}')

        if ret.returncode < 0:
            return {'state': 4, 'data': f'{args["module"]}自动化测试未正常运行，请查看日志'}

        html_report_path = f"{project_path}/backend/templates/{args['module']}_report.html"
        result = analysis_html_report(html_report_path)

        if bool(result['fail_result']):
            current_app.logger.info(result)
            state = 0

        return {'state': state, **result}

    def assert_is_test_run(self, pytest_result):
        run_result = pytest_result.strip().split('\n')[-1]
        result = ' '.join(run_result.split(' ')[1:-1])
        if not 'no test' in result:
            return False
        return True

    def get_run_pytest_cmd(self, module, project_path, ip_port):
        if ip_port is None:
            ip_port = ''
        else:
            ip_port = f'--ip_port {ip_port}'
        business_module = {
            'mainprocess': f'pytest {project_path}/tests/test_mainprocess/ --html=backend/templates/{module}_report.html --self-contained-html {ip_port}',
            'lg-zhaopin-boot': f'pytest {project_path}/tests/test_lg_zhaopin_boot/ --html=backend/templates/{module}_report.html --self-contained-html {ip_port}',
            'lg-entry-boot': f'pytest {project_path}/tests/test_lg_entry_boot/ --html=backend/templates/{module}_report.html --self-contained-html {ip_port}',
            'lg-neirong-boot': f'pytest {project_path}/tests/test_lg_neirong_boot/ --html=backend/templates/{module}_report.html --self-contained-html {ip_port}',
            'open_api_lagou': f'pytest {project_path}/tests/test_open_api_lagou_com/ --html=backend/templates/{module}_report.html --self-contained-html {ip_port}'

        }
        return business_module.get(module)

    def switch_project_root_directory(self):
        project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        os.chdir(project_path)
        return project_path
