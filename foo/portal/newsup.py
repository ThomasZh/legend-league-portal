#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2016 planc2c.com
# thomas@time2box.com
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.web
import logging
import time
import sys
import os
import uuid
import smtplib
import json as JSON # 启用别名，不会跟方法里的局部变量混淆
from bson import json_util

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../dao"))

from tornado.escape import json_encode, json_decode
from tornado.httpclient import *
from tornado.httputil import url_concat
from bson import json_util

from comm import *
from global_const import *


class WxMpVerifyHandler(tornado.web.RequestHandler):
    def get(self):
        self.finish('qdkkOWgyqqLTrijx')
        return


class NewsupLoginNextHandler(tornado.web.RequestHandler):
    def get(self):
        login_next = self.get_secure_cookie("login_next")
        logging.info("got login_next %r",login_next)
        if login_next:
            self.redirect(login_next)
        else:
            self.redirect("/portal/newsup/index")


class NewsupIndexHandler(BaseHandler):
    def get(self):
        logging.info(self.request)

        # league(联盟信息)
        league_info = self.get_league_info()

        # franchises(景区)
        params = {"filter":"league", "franchise_type":"景区", "page":1, "limit":5}
        url = url_concat(API_DOMAIN+"/api/leagues/"+LEAGUE_ID+"/clubs", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        rs = data['rs']
        franchises = rs['data']
        for franchise in franchises:
            franchise['create_time'] = timestamp_friendly_date(franchise['create_time'])

        # suppliers(供应商)
        params = {"filter":"league", "franchise_type":"供应商", "page":1, "limit":5}
        url = url_concat(API_DOMAIN+"/api/leagues/"+LEAGUE_ID+"/clubs", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        rs = data['rs']
        suppliers = rs['data']
        for supplier in suppliers:
            supplier['create_time'] = timestamp_friendly_date(supplier['create_time'])

        # sceneries(景点)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"41c057a6f73411e69a3c00163e023e51", "idx":0, "limit":5}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        sceneries = data['rs']
        for article in sceneries:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # journey(游记)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"01d6120cf73411e69a3c00163e023e51", "idx":0, "limit":12}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        journeies = data['rs']
        for article in journeies:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # activity(活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        activities = data['rs']

        # recently articles(最新文章news)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        news = data['rs']
        for article in news:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        populars = data['rs']
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # hot(热点新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"1b86ad38f73411e69a3c00163e023e51", "idx":0, "limit":12}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        hots = data['rs']
        for article in hots:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat(API_DOMAIN+"/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        lastest_comments = data['rs']
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        # multimedia
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":8}
        url = url_concat(API_DOMAIN+"/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        multimedias = data['rs']
        for multimedia in multimedias:
            multimedia['publish_time'] = timestamp_friendly_date(multimedia['publish_time'])

        # notices
        params = {"filter":"league", "league_id":LEAGUE_ID, "page":1, "limit":3}
        url = url_concat(API_DOMAIN+"/api/notice-board", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        notices = data['rs']

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token>>>>> %r",access_token)
        if access_token:
            is_login = True

        self.render('newsup/index.html',
                is_login=is_login,
                franchises=franchises,
                suppliers=suppliers,
                sceneries=sceneries,
                journeies=journeies,
                news=news,
                populars=populars,
                hots=hots,
                league_info=league_info,
                activities=activities,
                lastest_comments=lastest_comments,
                multimedias=multimedias,
                api_domain=API_DOMAIN,
                notices=notices['data'])


class NewsupAccountHandler(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        # league(联盟信息)
        league_info = self.get_league_info()

        headers = {"Authorization":"Bearer "+access_token}
        url = API_DOMAIN+"/api/myinfo?filter=login"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET", headers=headers)
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        user = data['rs']

        self.render('newsup/account.html',
                is_login=is_login,
                league_info=league_info,
                user = user,
                access_token=access_token,
                api_domain=API_DOMAIN,
                upyun_domain=UPYUN_DOMAIN,
                upyun_notify_url=UPYUN_NOTIFY_URL,
                upyun_form_api_secret=UPYUN_FORM_API_SECRET,
                upyun_bucket=UPYUN_BUCKET)


class NewsupAuthorHandler(BaseHandler):
    def get(self):
        logging.info(self.request)
        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        # league(联盟信息)
        league_info = self.get_league_info()

        # news(新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"30a56cb8f73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        news = data['rs']
        for article in news:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        populars = data['rs']
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # activity(活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        activities = data['rs']

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat(API_DOMAIN+"/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        lastest_comments = data['rs']
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        self.render('newsup/author.html',
                is_login=is_login,
                league_info=league_info,
                news=news,
                populars=populars,
                activities=activities,
                api_domain=API_DOMAIN,
                lastest_comments=lastest_comments)


class NewsupMediaHandler(BaseHandler):
    def get(self):
        logging.info(self.request)

        # league(联盟信息)
        league_info = self.get_league_info()

        # multimedia
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":14}
        url = url_concat(API_DOMAIN+"/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        multimedias = data['rs']

        # news(新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"30a56cb8f73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        news = data['rs']
        for article in news:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # hot(热点新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"1b86ad38f73411e69a3c00163e023e51", "idx":0, "limit":12}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        hots = data['rs']
        for article in hots:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        populars = data['rs']
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # activity(活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        activities = data['rs']

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat(API_DOMAIN+"/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        lastest_comments = data['rs']
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/media.html',
                is_login=is_login,
                league_info=league_info,
                news=news,
                populars=populars,
                activities=activities,
                hots=hots,
                lastest_comments=lastest_comments,
                league_id=LEAGUE_ID,
                api_domain=API_DOMAIN,
                multimedias=multimedias)


class NewsupShortcodesHandler(BaseHandler):
    def get(self):
        logging.info(self.request)

        # league(联盟信息)
        league_info = self.get_league_info()

        # news(新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"30a56cb8f73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        news = data['rs']
        for article in news:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        populars = data['rs']
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # activity(活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        activities = data['rs']

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/shortcodes.html',
                is_login=is_login,
                league_info=league_info,
                news=news,
                activities=activities,
                api_domain=API_DOMAIN,
                populars=populars)


class NewsupContactHandler(BaseHandler):
    def get(self):
        logging.info(self.request)

        # league(联盟信息)
        league_info = self.get_league_info()

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat(API_DOMAIN+"/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        lastest_comments = data['rs']
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/contact.html',
                is_login=is_login,
                league_info=league_info,
                lastest_comments=lastest_comments,
                api_domain=API_DOMAIN,
                league_id=LEAGUE_ID)


class NewsupItemDetailHandler(BaseHandler):
    def get(self):
        logging.info(self.request)
        article_id = self.get_argument("id", "")

        # league(联盟信息)
        league_info = self.get_league_info()

        # recently articles(最新文章news)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        news = data['rs']
        for article in news:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        populars = data['rs']
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # activity(活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        activities = data['rs']

        # article
        url = API_DOMAIN+"/api/articles/"+article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got article response %r", response.body)
        data = json_decode(response.body)
        article_info = data['rs']
        article_info['publish_time'] = timestamp_friendly_date(article_info['publish_time'])

        # hot(热点新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"1b86ad38f73411e69a3c00163e023e51", "idx":0, "limit":12}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        hots = data['rs']
        for article in hots:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # update read_num
        read_num = article_info['read_num']
        url = API_DOMAIN+"/api/articles/"+article_id+"/read"
        http_client = HTTPClient()
        _body = {"read_num": read_num+1}
        _json = json_encode(_body)
        response = http_client.fetch(url, method="POST", body=_json)
        logging.info("got update read_num response %r", response.body)

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat(API_DOMAIN+"/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        lastest_comments = data['rs']
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        # multimedia
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        multimedias = data['rs']

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/item-detail.html',
                is_login=is_login,
                access_token=access_token,
                league_info=league_info,
                article_info=article_info,
                news=news,
                populars=populars,
                hots=hots,
                activities=activities,
                api_domain=API_DOMAIN,
                multimedias=multimedias,
                lastest_comments=lastest_comments)


class NewsupNewHandler(BaseHandler):
    def get(self):
        logging.info(self.request)

        # league(联盟信息)
        league_info = self.get_league_info()

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/new.html',
                league_info=league_info,
                api_domain=API_DOMAIN,
                is_login=is_login)


class NewsupCategoryTileHandler(BaseHandler):
    def get(self):
        logging.info(self.request)

        # league(联盟信息)
        league_info = self.get_league_info()

        # recently articles(最新文章news)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        news = data['rs']
        for article in news:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        populars = data['rs']
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # activity(活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        activities = data['rs']

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat(API_DOMAIN+"/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        lastest_comments = data['rs']
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/category-tile.html',
                is_login=is_login,
                league_info=league_info,
                lastest_comments=lastest_comments,
                news=news,
                activities=activities,
                api_domain=API_DOMAIN,
                populars=populars)


class NewsupCategoryHandler(BaseHandler):
    def get(self):
        logging.info(self.request)
        category_id = self.get_argument("id", "")

        # league(联盟信息)
        league_info = self.get_league_info()

        # query category_name by category_id
        url = API_DOMAIN+"/api/categories/" + category_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        category = data['rs']

        # query by category_id
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":category_id, "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        sceneries = data['rs']
        for article in sceneries:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # multimedia
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        multimedias = data['rs']

        # recently articles(最新文章news)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        news = data['rs']
        for article in news:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        populars = data['rs']
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # activity(活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        activities = data['rs']

        # hot(热点新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"1b86ad38f73411e69a3c00163e023e51", "idx":0, "limit":12}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        hots = data['rs']
        for article in hots:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat(API_DOMAIN+"/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        lastest_comments = data['rs']
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/category.html',
                is_login=is_login,
                league_info=league_info,
                sceneries=sceneries,
                news=news,
                hots=hots,
                populars=populars,
                activities=activities,
                lastest_comments=lastest_comments,
                multimedias=multimedias,
                league_id=LEAGUE_ID,
                category_id=category_id,
                api_domain=API_DOMAIN,
                category=category)


class NewsupCategorySearchHandler(BaseHandler):
    def get(self):
        logging.info(self.request)
        category_id = self.get_argument("id", "")

        # league(联盟信息)
        league_info = self.get_league_info()

        # query category_name by category_id
        url = API_DOMAIN+"/api/categories/" + category_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        category = data['rs']

        # query by category_id
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":category_id, "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        sceneries = data['rs']
        for article in sceneries:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # multimedia
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        multimedias = data['rs']

        # recently articles(最新文章news)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        news = data['rs']
        for article in news:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        populars = data['rs']
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # activity(活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        activities = data['rs']

        # hot(热点新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"1b86ad38f73411e69a3c00163e023e51", "idx":0, "limit":12}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        hots = data['rs']
        for article in hots:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat(API_DOMAIN+"/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        lastest_comments = data['rs']
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/category-search.html',
                is_login=is_login,
                league_info=league_info,
                sceneries=sceneries,
                news=news,
                hots=hots,
                populars=populars,
                activities=activities,
                lastest_comments=lastest_comments,
                multimedias=multimedias,
                league_id=LEAGUE_ID,
                category_id=category_id,
                api_domain=API_DOMAIN,
                category=category)


class NewsupFranchisesHandler(BaseHandler):
    def get(self):
        logging.info(self.request)
        franchise_type = self.get_argument("franchise_type", "")
        franchise_type = franchise_type.encode('utf-8')
        logging.info("got franchise_type %r from argument", franchise_type)

        # league(联盟信息)
        league_info = self.get_league_info()

        # franchises(景区)
        params = {"franchise_type":franchise_type, "page":1, "limit":1}
        url = url_concat(API_DOMAIN+"/api/leagues/"+LEAGUE_ID+"/clubs", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        franchises = data['rs']['data']
        for franchise in franchises:
            franchise['create_time'] = timestamp_friendly_date(franchise['create_time'])

        # multimedia
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        multimedias = data['rs']

        # recently articles(最新文章news)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        news = data['rs']
        for article in news:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        populars = data['rs']
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # activity(活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        activities = data['rs']

        # hot(热点新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"1b86ad38f73411e69a3c00163e023e51", "idx":0, "limit":12}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        hots = data['rs']
        for article in hots:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat(API_DOMAIN+"/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        lastest_comments = data['rs']
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/franchises.html',
                is_login=is_login,
                league_info=league_info,
                franchises=franchises,
                multimedias=multimedias,
                news=news,
                hots= hots,
                populars=populars,
                activities=activities,
                lastest_comments=lastest_comments,
                league_id=LEAGUE_ID,
                api_domain=API_DOMAIN,
                franchise_type=franchise_type)


class NewsupFranchiseDetailHandler(BaseHandler):
    def get(self):
        logging.info(self.request)
        franchise_id = self.get_argument("id", "")
        access_token = self.get_secure_cookie("access_token")
        # league(联盟信息)
        league_info = self.get_league_info()

        # recently articles(最新文章news)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        news = data['rs']
        for article in news:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        populars = data['rs']
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # activity(活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        activities = data['rs']

        # article
        url = API_DOMAIN+"/api/clubs/"+franchise_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got article response %r", response.body)
        data = json_decode(response.body)
        franchise = data['rs']
        if not franchise.has_key('paragraphs'):
            franchise['paragraphs'] = ''
        if not franchise.has_key('franchise_type'):
            franchise['franchise_type'] = 'franchise'
        if franchise.has_key('create_time'):
            franchise['create_time'] = timestamp_friendly_date(franchise['create_time'])
        else:
            franchise['create_time'] = timestamp_friendly_date(0)
        # franchise['create_time'] = timestamp_friendly_date(franchise['create_time'])

        # hot(热点新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"1b86ad38f73411e69a3c00163e023e51", "idx":0, "limit":12}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        hots = data['rs']
        for article in hots:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # update read_num
        read_num = franchise['read_num']
        url = API_DOMAIN+"/api/articles/"+franchise_id+"/read"
        http_client = HTTPClient()
        _body = {"read_num": read_num+1}
        _json = json_encode(_body)
        response = http_client.fetch(url, method="POST", body=_json)
        logging.info("got update read_num response %r", response.body)

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat(API_DOMAIN+"/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        lastest_comments = data['rs']
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        # multimedia
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        multimedias = data['rs']

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/franchise-detail.html',
                is_login=is_login,
                access_token=access_token,
                league_info=league_info,
                franchise=franchise,
                news=news,
                populars=populars,
                hots=hots,
                activities=activities,
                multimedias=multimedias,
                api_domain=API_DOMAIN,
                lastest_comments=lastest_comments)


class NewsupApplyFranchiseHandler(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        logging.info(self.request)

        # league(联盟信息)
        league_info = self.get_league_info()

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        franchise = None
        try:
            params = {"filter":"franchise"}
            url = url_concat(API_DOMAIN+"/api/myinfo", params)
            http_client = HTTPClient()
            headers={"Authorization":"Bearer "+access_token}
            response = http_client.fetch(url, method="GET", headers=headers)
            logging.info("got response %r", response.body)
            data = json_decode(response.body)
            franchise = data['rs']
            if franchise:
                if not franchise['club'].has_key("province"):
                    franchise['club']['province'] = ''
                    franchise['club']['city'] = ''
                if not franchise['club'].has_key("city"):
                    franchise['club']['city'] = ''
                if not franchise['club'].has_key("franchise_type"):
                    franchise['club']['franchise_type'] = ''
                franchise['create_time'] = timestamp_datetime(franchise['create_time'])
        except:
            logging.info("got franchise=[None]")

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat(API_DOMAIN+"/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        lastest_comments = data['rs']
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        self.render('newsup/apply-franchise.html',
                is_login=is_login,
                league_info=league_info,
                access_token=access_token,
                league_id=LEAGUE_ID,
                franchise=franchise,
                api_domain=API_DOMAIN,
                upyun_domain=UPYUN_DOMAIN,
                upyun_notify_url=UPYUN_NOTIFY_URL,
                upyun_form_api_secret=UPYUN_FORM_API_SECRET,
                upyun_bucket=UPYUN_BUCKET,
                lastest_comments=lastest_comments)


class NewsupSearchResultHandler(BaseHandler):
    def get(self):
        logging.info(self.request)
        # category_id = self.get_argument("id", "")

        # league(联盟信息)
        league_info = self.get_league_info()

        # query by category_id
        # params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":category_id, "idx":0, "limit":6}
        # url = url_concat(API_DOMAIN+"/api/articles", params)
        # http_client = HTTPClient()
        # response = http_client.fetch(url, method="GET")
        # logging.info("got sceneries response %r", response.body)
        # data = json_decode(response.body)
        # sceneries = data['rs']
        # for article in sceneries:
        #     article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # multimedia
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        multimedias = data['rs']

        # news(新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0e9a3c68e94511e6b40600163e023e51", "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        news = data['rs']
        for article in news:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        populars = data['rs']
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # activity(活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        activities = data['rs']

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat(API_DOMAIN+"/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        lastest_comments = data['rs']
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/search-result.html',
                is_login=is_login,
                league_info=league_info,
                news=news,
                populars=populars,
                activities=activities,
                lastest_comments=lastest_comments,
                multimedias=multimedias,
                league_id=LEAGUE_ID,
                api_domain=API_DOMAIN)
