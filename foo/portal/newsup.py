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


class NewsupLoginNextHandler(tornado.web.RequestHandler):
    def get(self):
        login_next = self.get_secure_cookie("login_next")
        if login_next:
            self.redirect(login_next)
        else:
            self.redirect("/portal/newsup/index")


class NewsupIndexHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)

        # sceneries(景点)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"41c057a6f73411e69a3c00163e023e51", "idx":0, "limit":5}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        sceneries = json_decode(response.body)
        for article in sceneries:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # journey(游记)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"01d6120cf73411e69a3c00163e023e51", "idx":0, "limit":5}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        journeies = json_decode(response.body)
        for article in journeies:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # activity(活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        activities = json_decode(response.body)

        # news(新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"30a56cb8f73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        news = json_decode(response.body)
        for article in news:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        populars = json_decode(response.body)
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # hot(热点新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"1b86ad38f73411e69a3c00163e023e51", "idx":0, "limit":12}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        hots = json_decode(response.body)
        for article in hots:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat("http://api.7x24hs.com/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        lastest_comments = json_decode(response.body)
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        # multimedia
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":8}
        url = url_concat("http://api.7x24hs.com/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        multimedias = json_decode(response.body)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/index.html',
                is_login=is_login,
                sceneries=sceneries,
                journeies=journeies,
                news=news,
                populars=populars,
                hots=hots,
                activities=activities,
                lastest_comments=lastest_comments,
                multimedias=multimedias)


class NewsupAccountHandler(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        logging.info(self.request)
        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        headers = {"Authorization":"Bearer "+access_token}
        url = "http://api.7x24hs.com/api/myinfo"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET", headers=headers)
        logging.info("got response %r", response.body)
        user = json_decode(response.body)

        self.render('newsup/account.html',
                is_login=is_login,
                user = user)


class NewsupAuthorHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        # news(新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"30a56cb8f73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        news = json_decode(response.body)
        for article in news:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        populars = json_decode(response.body)
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # activity(活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        activities = json_decode(response.body)

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat("http://api.7x24hs.com/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        lastest_comments = json_decode(response.body)
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        self.render('newsup/author.html',
                is_login=is_login,
                news=news,
                populars=populars,
                activities=activities,
                lastest_comments=lastest_comments)


class NewsupMediaHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)

        # multimedia
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":14}
        url = url_concat("http://api.7x24hs.com/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        multimedias = json_decode(response.body)

        # news(新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"30a56cb8f73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        news = json_decode(response.body)
        for article in news:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        populars = json_decode(response.body)
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # activity(活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        activities = json_decode(response.body)

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat("http://api.7x24hs.com/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        lastest_comments = json_decode(response.body)
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/media.html',
                is_login=is_login,
                news=news,
                populars=populars,
                activities=activities,
                lastest_comments=lastest_comments,
                league_id=LEAGUE_ID,
                multimedias=multimedias)


class NewsupShortcodesHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)

        # news(新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"30a56cb8f73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        news = json_decode(response.body)
        for article in news:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        populars = json_decode(response.body)
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # activity(活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        activities = json_decode(response.body)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/shortcodes.html',
                is_login=is_login,
                news=news,
                activities=activities,
                populars=populars)


class NewsupContactHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat("http://api.7x24hs.com/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        lastest_comments = json_decode(response.body)
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/contact.html',
                is_login=is_login,
                lastest_comments=lastest_comments)


class NewsupItemDetailHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        article_id = self.get_argument("id", "")

        # news(新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"30a56cb8f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        news = json_decode(response.body)
        for article in news:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        populars = json_decode(response.body)
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # activity(活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        activities = json_decode(response.body)

        # article
        url = "http://api.7x24hs.com/api/articles/"+article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got article response %r", response.body)
        article_info = json_decode(response.body)
        article_info['publish_time'] = timestamp_friendly_date(article_info['publish_time'])

        # update view_num
        view_num = article_info['view_num']
        url = "http://api.7x24hs.com/api/articles/"+article_id+"/read"
        http_client = HTTPClient()
        _body = {"view_num": view_num+1}
        _json = json_encode(_body)
        response = http_client.fetch(url, method="POST", body=_json)
        logging.info("got update view_num response %r", response.body)

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat("http://api.7x24hs.com/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        lastest_comments = json_decode(response.body)
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        # multimedia
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":4}
        url = url_concat("http://api.7x24hs.com/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        multimedias = json_decode(response.body)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/item-detail.html',
                is_login=is_login,
                article_info=article_info,
                news=news,
                populars=populars,
                activities=activities,
                multimedias=multimedias,
                lastest_comments=lastest_comments)


class NewsupNewHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/new.html',
                is_login=is_login)


class NewsupCategoryTileHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)

        # news(新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"30a56cb8f73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        news = json_decode(response.body)
        for article in news:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        populars = json_decode(response.body)
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # activity(活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        activities = json_decode(response.body)

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat("http://api.7x24hs.com/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        lastest_comments = json_decode(response.body)
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/category-tile.html',
                is_login=is_login,
                lastest_comments=lastest_comments,
                news=news,
                activities=activities,
                populars=populars)


class NewsupCategoryHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        category_id = self.get_argument("id", "")

        # query category_name by category_id
        url = "http://api.7x24hs.com/api/categories/" + category_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        category = json_decode(response.body)

        # query by category_id
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":category_id, "idx":0, "limit":6}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        sceneries = json_decode(response.body)
        for article in sceneries:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # multimedia
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":4}
        url = url_concat("http://api.7x24hs.com/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        multimedias = json_decode(response.body)

        # news(新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0e9a3c68e94511e6b40600163e023e51", "idx":0, "limit":6}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        news = json_decode(response.body)
        for article in news:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        populars = json_decode(response.body)
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # activity(活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        activities = json_decode(response.body)

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat("http://api.7x24hs.com/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        lastest_comments = json_decode(response.body)
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/category.html',
                is_login=is_login,
                sceneries=sceneries,
                news=news,
                populars=populars,
                activities=activities,
                lastest_comments=lastest_comments,
                multimedias=multimedias,
                league_id=LEAGUE_ID,
                category_id=category_id,
                category=category)


class NewsupFranchiseHandler(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        url = "http://api.7x24hs.com/api/myinfo/franchises"
        http_client = HTTPClient()
        headers={"Authorization":"Bearer "+access_token}
        response = http_client.fetch(url, method="GET", headers=headers)
        logging.info("got response %r", response.body)
        franchises = json_decode(response.body)
        franchise_in_this_league = None
        for franchise in franchises:
            franchise['create_time'] = timestamp_datetime(franchise['create_time'])
            if franchise['league_id'] == LEAGUE_ID:
                franchise_in_this_league = franchise

                break

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat("http://api.7x24hs.com/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        lastest_comments = json_decode(response.body)
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        self.render('newsup/franchise.html',
                is_login=is_login,
                league_id=LEAGUE_ID,
                franchise=franchise_in_this_league,
                lastest_comments=lastest_comments)


class NewsupSearchResultHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        category_id = self.get_argument("id", "")

        # query by category_id
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":category_id, "idx":0, "limit":6}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        sceneries = json_decode(response.body)
        for article in sceneries:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # multimedia
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":4}
        url = url_concat("http://api.7x24hs.com/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        multimedias = json_decode(response.body)

        # news(新闻)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0e9a3c68e94511e6b40600163e023e51", "idx":0, "limit":6}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        news = json_decode(response.body)
        for article in news:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":6}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        populars = json_decode(response.body)
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # activity(活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":4}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        activities = json_decode(response.body)

        # lastest comments(最新的评论)
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        url = url_concat("http://api.7x24hs.com/api/last-comments", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        lastest_comments = json_decode(response.body)
        for comment in lastest_comments:
            comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/search-result.html',
                is_login=is_login,
                sceneries=sceneries,
                news=news,
                populars=populars,
                activities=activities,
                lastest_comments=lastest_comments,
                multimedias=multimedias,
                league_id=LEAGUE_ID,
                category_id=category_id)
