import pytest
from api_script.jianzhao_web.b_basic.b_upload import upload_permit
from api_script.jianzhao_web.b_basic.company import jump_step1, jump_html
from api_script.jianzhao_web.b_basic.toB_saveHR_1 import saveHR, add_saveCompany, submit_new
from api_script.neirong_app.account import upate_user_password
from utils.read_file import record_cancel_account
from utils.util import assert_equal, pc_send_register_verifyCode, verify_code_message, login_password, \
    user_register_lagou
from .test_1_create_company import skip_

register_state = 1
skip_1 = pytest.mark.skipif('register_state != 1', reason='注册失败,跳过执行')


@skip_
def test_register_general_user(get_countryCode_phone_general_user):
    global general_countryCode, general_phone, general_user_name, verify_code
    general_countryCode, general_phone, general_user_name = get_countryCode_phone_general_user[0], \
                                                            get_countryCode_phone_general_user[1], \
                                                            get_countryCode_phone_general_user[2]
    global register_state
    if pc_send_register_verifyCode(general_countryCode, general_phone) == 1:
        verify_code = verify_code_message(general_countryCode, general_phone)
        assert_equal(True, bool(verify_code), '获取验证码成功')
        register = user_register_lagou(general_countryCode, general_phone, verify_code)
        register_state = register.get('state', 0)
        assert_equal(1, register['state'], "校验普通用户注册是否成功", '失败手机号:{}'.format(general_countryCode + general_phone))
    else:
        record_cancel_account(general_countryCode + general_phone)
        register_state = 2
        assert_equal(1, register_state, '校验发送验证码是否成功', '失败手机号:{}'.format(general_countryCode + general_phone))


@skip_1
@skip_
def test_general_user_join_company(get_company_name):
    personal_msg_save = saveHR(get_company_name, general_user_name, 'ariaxie@lagou.com', '技术总监')
    if personal_msg_save['state'] == 1:
        join_company = add_saveCompany()
        assert_equal(1, join_company['state'], "校验加入公司是否成功")
    else:
        assert_equal(1, personal_msg_save['state'], "校验保存用户信息是否成功")


@skip_1
@skip_
def test_jump_html():
    save_result = jump_html()
    assert_equal(1, save_result['state'], '校验是否跳过选择优质简历')


@skip_1
@skip_
def test_general_personal_certificate():
    upload_p = upload_permit()
    if upload_p['state'] == 1:
        personal_certificate_submit = submit_new()
        assert_equal(1, personal_certificate_submit['state'], "校验提交招聘者身份审核是否成功")
    else:
        assert_equal(1, upload_p['state'], "校验提交身份信息是否成功")


@skip_1
@skip_
@pytest.mark.parametrize('newPassword', [('990eb670f81e82f546cfaaae1587279a')])
def test_update_general_user(newPassword):
    r = upate_user_password(newPassword)
    assert_equal(1, r['state'], '普通用户修改密码成功')
