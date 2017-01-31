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
from foo.portal import portal_newsup


def map():

    config = [

        # homepage
        (r'/', getattr(portal_newsup, 'NewsupIndexHandler')),

        (r'/portal/newsup/index', getattr(portal_newsup, 'NewsupIndexHandler')),
        (r'/portal/newsup/account', getattr(portal_newsup, 'NewsupAccountHandler')),
        (r'/portal/newsup/author', getattr(portal_newsup, 'NewsupAuthorHandler')),
        (r'/portal/newsup/media', getattr(portal_newsup, 'NewsupMediaHandler')),
        (r'/portal/newsup/shortcodes', getattr(portal_newsup, 'NewsupShortcodesHandler')),
        (r'/portal/newsup/contact', getattr(portal_newsup, 'NewsupContactHandler')),
        (r'/portal/newsup/item-detail', getattr(portal_newsup, 'NewsupItemDetailHandler')),
        (r'/portal/newsup/new', getattr(portal_newsup, 'NewsupNewHandler')),
        (r'/portal/newsup/register', getattr(portal_newsup, 'NewsupRegisterHandler')),
        (r'/portal/newsup/category', getattr(portal_newsup, 'NewsupCategoryHandler')),
        (r'/portal/newsup/franchise', getattr(portal_newsup, 'NewsupFranchiseHandler')),


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
        # 认证页面
        (r'/uicn/cert', getattr(ui_cn, 'UicnCertHandler')),

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
        (r'/portal/auth/logout', getattr(auth_email, 'AuthLogoutHandler')),

        # comm
        ('.*', getattr(comm, 'PageNotFoundHandler'))

    ]

    return config
