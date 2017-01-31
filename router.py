# _*_ coding: utf-8_*_
#
# genral application route config:
# simplify the router config by dinamic load class
# by lwz7512
# @2016/05/17

import tornado.web

from foo import comm
from foo.auth import auth_newsup
from foo.portal import portal_newsup


def map():

    config = [

        # homepage
        (r'/', getattr(portal_newsup, 'NewsupIndexHandler')),

        # login_next redirect to index
        # 页面重定向后，可以将cookie加载
        (r'/portal/newsup/login-next', getattr(portal_newsup, 'NewsupLoginNextHandler')),
        (r'/portal/newsup/index', getattr(portal_newsup, 'NewsupIndexHandler')),
        (r'/portal/newsup/account', getattr(portal_newsup, 'NewsupAccountHandler')),
        (r'/portal/newsup/author', getattr(portal_newsup, 'NewsupAuthorHandler')),
        (r'/portal/newsup/media', getattr(portal_newsup, 'NewsupMediaHandler')),
        (r'/portal/newsup/shortcodes', getattr(portal_newsup, 'NewsupShortcodesHandler')),
        (r'/portal/newsup/contact', getattr(portal_newsup, 'NewsupContactHandler')),
        (r'/portal/newsup/item-detail', getattr(portal_newsup, 'NewsupItemDetailHandler')),
        (r'/portal/newsup/new', getattr(portal_newsup, 'NewsupNewHandler')),
        (r'/portal/newsup/category', getattr(portal_newsup, 'NewsupCategoryHandler')),
        (r'/portal/newsup/franchise', getattr(portal_newsup, 'NewsupFranchiseHandler')),

        (r'/portal/auth/register', getattr(auth_newsup, 'AuthRegisterHandler')),
        (r'/portal/auth/login', getattr(auth_newsup, 'AuthRegisterHandler')),
        (r'/portal/auth/lost-pwd', getattr(auth_newsup, 'AuthRegisterHandler')),
        (r'/portal/auth/logout', getattr(auth_newsup, 'AuthLogoutHandler')),
        (r'/portal/auth/league-signup', getattr(auth_newsup, 'AuthLeagueSignupXHR')),

        # comm
        ('.*', getattr(comm, 'PageNotFoundHandler'))

    ]

    return config
