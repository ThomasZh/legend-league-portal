# _*_ coding: utf-8_*_
#
# genral application route config:
# simplify the router config by dinamic load class
# by lwz7512
# @2016/05/17

import tornado.web

from foo import comm
from foo.auth import auth_newsup
from foo.portal import newsup


def map():

    config = [

        # homepage
        (r'/', getattr(newsup, 'NewsupIndexHandler')),

        (r'/MP_verify_qdkkOWgyqqLTrijx.txt', getattr(newsup, 'WxMpVerifyHandler')),

        # login_next redirect to index
        # 页面重定向后，可以将cookie加载
        (r'/portal/newsup/login-next', getattr(newsup, 'NewsupLoginNextHandler')),
        (r'/portal/newsup/index', getattr(newsup, 'NewsupIndexHandler')),
        (r'/portal/newsup/account', getattr(newsup, 'NewsupAccountHandler')),
        (r'/portal/newsup/author', getattr(newsup, 'NewsupAuthorHandler')),
        (r'/portal/newsup/media', getattr(newsup, 'NewsupMediaHandler')),
        (r'/portal/newsup/shortcodes', getattr(newsup, 'NewsupShortcodesHandler')),
        (r'/portal/newsup/contact', getattr(newsup, 'NewsupContactHandler')),
        (r'/portal/newsup/item-detail', getattr(newsup, 'NewsupItemDetailHandler')),
        (r'/portal/newsup/new', getattr(newsup, 'NewsupNewHandler')),
        (r'/portal/newsup/category', getattr(newsup, 'NewsupCategoryHandler')),
        (r'/portal/newsup/category-search', getattr(newsup, 'NewsupCategorySearchHandler')),
        (r'/portal/newsup/category-tile', getattr(newsup, 'NewsupCategoryTileHandler')),
        (r'/portal/newsup/franchises', getattr(newsup, 'NewsupFranchisesHandler')),
        (r'/portal/newsup/franchise-detail', getattr(newsup, 'NewsupFranchiseDetailHandler')),
        (r'/portal/newsup/apply-franchise', getattr(newsup, 'NewsupApplyFranchiseHandler')),
        (r'/portal/newsup/search', getattr(newsup, 'NewsupSearchResultHandler')),

        (r'/portal/newsup/ticket-list', getattr(newsup, 'NewsupTicketListHandler')),
        (r'/portal/newsup/ticket-cart', getattr(newsup, 'NewsupTicketCartHandler')),
        (r'/portal/newsup/pay-style', getattr(newsup, 'NewsupTicketBalanceHandler')),
        (r'/portal/newsup/order-list', getattr(newsup, 'NewsupOrderListHandler')),

        (r'/api/portal/newsup/articles', getattr(newsup, 'ApiArticlesXHR')), #获取文章数据api


        (r'/portal/auth/register', getattr(auth_newsup, 'AuthRegisterHandler')),
        (r'/portal/auth/login', getattr(auth_newsup, 'AuthLoginHandler')),
        (r'/portal/auth/lost-pwd', getattr(auth_newsup, 'AuthLostpwdHandler')),
        (r'/portal/auth/logout', getattr(auth_newsup, 'AuthLogoutHandler')),
        (r'/portal/auth/league-signup', getattr(auth_newsup, 'AuthLeagueSignupXHR')),

        # comm
        ('.*', getattr(comm, 'PageNotFoundHandler'))

    ]

    return config
