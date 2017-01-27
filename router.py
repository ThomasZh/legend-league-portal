# _*_ coding: utf-8_*_
#
# genral application route config:
# simplify the router config by dinamic load class
# by lwz7512
# @2016/05/17

import tornado.web

from foo import comm
from foo.ui import ui_cn
from foo.auth import auth_email


def map():

    config = [

        # GET: 根据 HTTP header 收集客户端相关信息：是否手机、操作系统、浏览器等信息。
        (r'/', getattr(ui_cn, 'UicnIndexHandler')),

        (r'/uicn', getattr(ui_cn, 'UicnIndexHandler')),
        (r'/uicn/list', getattr(ui_cn, 'UicnListHandler')),
        (r'/uicn/exp', getattr(ui_cn, 'UicnExpHandler')),
        (r'/uicn/book', getattr(ui_cn, 'UicnBookHandler')),
        (r'/uicn/study', getattr(ui_cn, 'UicnStudyHandler')),
        (r'/uicn/game', getattr(ui_cn, 'UicnGameHandler')),
        (r'/uicn/peixun', getattr(ui_cn, 'UicnPeixunHandler')),
        (r'/uicn/topic', getattr(ui_cn, 'UicnTopicHandler')),
        (r'/uicn/online', getattr(ui_cn, 'UicnOnlineHandler')),
        (r'/uicn/zhaopin', getattr(ui_cn, 'UicnZhaopinHandler')),

        # 注册 登录 找回
        (r'/auth/login', getattr(ui_cn, 'AuthLoginHandler')),
        (r'/auth/getpass', getattr(ui_cn, 'AuthGetpassHandler')),
        (r'/auth/reg', getattr(ui_cn, 'AuthRegHandler')),
        (r'/auth/findpassbymail', getattr(ui_cn, 'AuthFindpassHandler')),
        (r'/auth/changepass', getattr(ui_cn, 'AuthChangepassHandler')),
        (r'/auth/editsuccess', getattr(ui_cn, 'AuthEditsuccessHandler')),

        (r'/portal/auth/login', getattr(auth_email, 'AuthEmailLoginHandler')),
        (r'/portal/auth/register', getattr(auth_email, 'AuthEmailRegisterHandler')),
        (r'/portal/auth/forgot-pwd', getattr(auth_email, 'AuthEmailForgotPwdHandler')),
        (r'/portal/auth/reset-pwd', getattr(auth_email, 'AuthEmailResetPwdHandler')),
        (r'/portal/auth/register/into-league', getattr(auth_email, 'AuthRegisterIntoLeagueXHR')),

        # comm
        ('.*', getattr(comm, 'PageNotFoundHandler'))

    ]

    return config
