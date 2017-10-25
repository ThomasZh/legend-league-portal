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
from urllib import urlencode
from urllib import unquote
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
        logging.info("^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^")
        logging.info("^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^")
        logging.info("GET %r", self.request.uri)

        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token=[%r]",access_token)

        login_next = self.get_secure_cookie("login_next")
        logging.info("got login_next=[%r]",login_next)
        if login_next:
            url = login_next
        else:
            url = "/portal/newsup/index"

        logging.info("OK(302): redirect to=[%r]", url)
        logging.info("~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~")
        logging.info("~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~")
        self.redirect(url)


class NewsupIndexHandler(BaseHandler):
    def get(self):
        logging.info(self.request)

        # league(联盟信息)
        league_info = self.get_league_info()

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token>>>>> %r",access_token)
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

        # activity(近期活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        activities = data['rs']
        for activitie in activities:
            activitie['publish_time'] = timestamp_friendly_date(activitie['publish_time'])

        # product(旅游产品)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"b0569f58144f11e78d3400163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        products = data['rs']
        for product in products:
            product['publish_time'] = timestamp_friendly_date(product['publish_time'])

        # requires(景区需求)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":'065f565e6bd711e7b46300163e023e51', "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        requires = data['rs']
        for article in requires:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # journey(旅游资讯)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"065f565e6bd711e7b46300163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        journeies = data['rs']
        for article in journeies:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # communities(经验交流)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"1b86ad38f73411e69a3c00163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        communities = data['rs']
        for article in communities:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # 一周热游榜(景区)
        second_categorys_id = "b8fa1f3ea41b11e7811500163e023e51"
        params = {"page":1, "limit":10}
        url = url_concat(API_DOMAIN+"/api/categories/"+second_categorys_id+"/clubs", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        rs = data['rs']
        hot_franchises = rs['data']

        # 当季热门
        second_categorys_id = "37eafe76b96b11e7a70e00163e023e51"
        params = {"page":1, "limit":10}
        url = url_concat(API_DOMAIN+"/api/categories/"+second_categorys_id+"/clubs", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        rs = data['rs']
        hot_tags = rs['data']

        # 热门景区
        hot_franchises_category_id = "757ee072a02511e7b7f600163e023e51"
        url = API_DOMAIN + "/api/def/categories/"+ hot_franchises_category_id +"/level2"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response.body %r", response.body)
        data = json_decode(response.body)
        hot_franchises_tags = data['rs']

        # franchises(热门景区列表)
        params = {"filter":"level1", "franchise_type":"scenery", "page":1, "limit":10, "category":hot_franchises_category_id}
        url = url_concat(API_DOMAIN+"/api/leagues/"+LEAGUE_ID+"/clubs-filter", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        rs = data['rs']
        franchises = rs['data']

        # 精彩推荐
        wonder_category_id = "8a8556c2a02511e7b7f600163e023e51"
        url = API_DOMAIN + "/api/def/categories/"+ wonder_category_id +"/level2"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response.body %r", response.body)
        data = json_decode(response.body)
        wonder_tags = data['rs']

        # franchises(精彩推荐景区列表)
        params = {"filter":"level1", "franchise_type":"scenery", "page":1, "limit":10, "category":wonder_category_id}
        url = url_concat(API_DOMAIN+"/api/leagues/"+LEAGUE_ID+"/clubs-filter", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        rs = data['rs']
        wonder_franchises = rs['data']

        #  特色路线
        feature_line_category_id = "b1fb3e94a1e011e7943000163e023e51"
        url = API_DOMAIN + "/api/def/categories/"+ feature_line_category_id +"/level2"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response.body %r", response.body)
        data = json_decode(response.body)
        feature_line_tags = data['rs']

        # franchises(特色路线列表)
        params = {"filter":"level1", "franchise_type":"scenery", "page":1, "limit":10, "category":feature_line_category_id}
        url = url_concat(API_DOMAIN+"/api/leagues/"+LEAGUE_ID+"/clubs-filter", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        rs = data['rs']
        feature_line_franchises = rs['data']

        self.render('newsup/index.html',
                api_domain=API_DOMAIN,
                league_info=league_info,
                is_login=is_login,
                is_ops=is_ops,
                franchises=franchises,
                activities=activities,
                products=products,
                requires=requires,
                journeies=journeies,
                communities=communities,
                hot_franchises=hot_franchises,
                hot_tags=hot_tags,
                hot_franchises_tags=hot_franchises_tags,
                wonder_tags=wonder_tags,
                wonder_franchises=wonder_franchises,
                feature_line_tags=feature_line_tags,
                feature_line_franchises=feature_line_franchises)


class NewsupAccountHandler(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

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
                is_ops=is_ops,
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

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

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
                is_ops=is_ops,
                league_info=league_info,
                news=news,
                populars=populars,
                activities=activities,
                api_domain=API_DOMAIN,
                lastest_comments=lastest_comments)


class NewsupMediaHandler(BaseHandler):
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

        # league(联盟信息)
        league_info = self.get_league_info()

        # product(旅游产品)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"b0569f58144f11e78d3400163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        products = data['rs']
        for product in products:
            product['publish_time'] = timestamp_friendly_date(product['publish_time'])

        # journey(旅游资讯)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"065f565e6bd711e7b46300163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        journeies = data['rs']
        for article in journeies:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # communities(经验交流)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"1b86ad38f73411e69a3c00163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        communities = data['rs']
        for article in communities:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # requires(景区需求)
        category_id = '065f565e6bd711e7b46300163e023e51'
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":category_id, "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        requires = data['rs']
        for article in requires:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

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

        self.render('newsup/media.html',
                is_login=is_login,
                is_ops=is_ops,
                league_info=league_info,
                products=products,
                journeies=journeies,
                communities=communities,
                requires=requires,
                lastest_comments=lastest_comments,
                league_id=LEAGUE_ID,
                api_domain=API_DOMAIN,
                multimedias=multimedias)


class NewsupShortcodesHandler(BaseHandler):
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

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

        self.render('newsup/shortcodes.html',
                is_login=is_login,
                is_ops=is_ops,
                league_info=league_info,
                news=news,
                activities=activities,
                api_domain=API_DOMAIN,
                populars=populars)


class NewsupContactHandler(BaseHandler):
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

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

        self.render('newsup/contact.html',
                is_login=is_login,
                is_ops=is_ops,
                access_token=access_token,
                league_info=league_info,
                lastest_comments=lastest_comments,
                api_domain=API_DOMAIN,
                league_id=LEAGUE_ID)


class NewsupItemDetailHandler(BaseHandler):
    def get(self):
        logging.info("^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^")
        logging.info("^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^")
        logging.info("GET %r", self.request.uri)

        article_id = self.get_argument("id", "")

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token=[%r]", access_token)
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

        # league(联盟信息)
        league_info = self.get_league_info()

        # article
        url = API_DOMAIN+"/api/articles/"+article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got article response %r", response.body)
        data = json_decode(response.body)
        article_info = data['rs']
        article_info['publish_time'] = timestamp_friendly_date(article_info['publish_time'])

        # club
        url = API_DOMAIN+"/api/clubs/"+article_info['club_id']
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got article response %r", response.body)
        data = json_decode(response.body)
        franchise = data['rs']

        # product(旅游产品)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"b0569f58144f11e78d3400163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        products = data['rs']
        for product in products:
            product['publish_time'] = timestamp_friendly_date(product['publish_time'])

        # journey(旅游资讯)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"065f565e6bd711e7b46300163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        journeies = data['rs']
        for article in journeies:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # last_activity(近期活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        last_activities = data['rs']
        for article in last_activities:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # communities(经验交流)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"1b86ad38f73411e69a3c00163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        communities = data['rs']
        for article in communities:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # requires(景区需求)
        category_id = '065f565e6bd711e7b46300163e023e51'
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":category_id, "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        requires = data['rs']
        for article in requires:
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
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        multimedias = data['rs']

        # franchise
        params = {"filter":"detail"}
        url = url_concat(API_DOMAIN+"/api/clubs/"+franchise['_id'],params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got article response %r", response.body)
        data = json_decode(response.body)
        franchise = data['rs']
        geo_x = franchise['gcj02']['x']
        geo_y = franchise['gcj02']['y']
        if not franchise.has_key('paragraphs'):
            franchise['paragraphs'] = ''
        if not franchise.has_key('franchise_type'):
            franchise['franchise_type'] = 'franchise'
        if franchise.has_key('create_time'):
            franchise['create_time'] = timestamp_friendly_date(franchise['create_time'])
        else:
            franchise['create_time'] = timestamp_friendly_date(0)

        url = API_DOMAIN+"/api/clubs/"+franchise['_id']+"/car-parks"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        parkings = data['rs']
        for parking in parkings:
            parking['percent'] = int(float(parking['remain_space']) / float(parking['max_space'])*100)
            logging.info("got parking %r", parking['percent'])

        self.render('newsup/item-detail.html',
                is_login=is_login,
                is_ops=is_ops,
                access_token=access_token,
                league_info=league_info,
                article_info=article_info,
                franchise=franchise,
                products=products,
                journeies=journeies,
                last_activities=last_activities,
                communities=communities,
                requires=requires,
                api_domain=API_DOMAIN,
                multimedias=multimedias,
                lastest_comments=lastest_comments,
                parkings=parkings,
                geo_x = geo_x,
                geo_y = geo_y)


class NewsupNewHandler(BaseHandler):
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

        # league(联盟信息)
        league_info = self.get_league_info()

        self.render('newsup/new.html',
                league_info=league_info,
                api_domain=API_DOMAIN,
                is_login=is_login,
                is_ops=is_ops)


class NewsupCategoryTileHandler(BaseHandler):
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

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

        self.render('newsup/category-tile.html',
                is_login=is_login,
                is_ops=is_ops,
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

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

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
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":category_id, "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        sceneries = data['rs']
        for article in sceneries:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # product(旅游产品)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"b0569f58144f11e78d3400163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got products response %r", response.body)
        data = json_decode(response.body)
        products = data['rs']
        for product in products:
            product['publish_time'] = timestamp_friendly_date(product['publish_time'])

        # journey(旅游资讯)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"065f565e6bd711e7b46300163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got journeies response %r", response.body)
        data = json_decode(response.body)
        journeies = data['rs']
        for article in journeies:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # communities(经验交流)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"1b86ad38f73411e69a3c00163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        communities = data['rs']
        for article in communities:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # requires(景区需求)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":'065f565e6bd711e7b46300163e023e51', "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        requires = data['rs']
        for article in requires:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # multimedia
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        multimedias = data['rs']
        for multimedia in multimedias:
            multimedia['publish_time'] = timestamp_friendly_date(multimedia['publish_time'])

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

        self.render('newsup/category.html',
                is_login=is_login,
                is_ops=is_ops,
                league_info=league_info,
                LEAGUE_ID = LEAGUE_ID,
                sceneries=sceneries,
                products=products,
                journeies=journeies,
                communities=communities,
                requires=requires,
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

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

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

        # product(旅游产品)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"b0569f58144f11e78d3400163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        products = data['rs']
        for product in products:
            product['publish_time'] = timestamp_friendly_date(product['publish_time'])

        # journey(旅游资讯)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"065f565e6bd711e7b46300163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        journeies = data['rs']
        for article in journeies:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # communities(经验交流)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"1b86ad38f73411e69a3c00163e023e51", "idx":0, "limit":12}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        communities = data['rs']
        for article in communities:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # requires(景区需求)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":'065f565e6bd711e7b46300163e023e51', "idx":0, "limit":12}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        requires = data['rs']
        for article in requires:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # multimedia
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        multimedias = data['rs']
        for multimedia in multimedias:
            multimedia['publish_time'] = timestamp_friendly_date(multimedia['publish_time'])

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

        self.render('newsup/category-search.html',
                is_login=is_login,
                is_ops=is_ops,
                league_info=league_info,
                sceneries=sceneries,
                products=products,
                journeies=journeies,
                communities=communities,
                requires=requires,
                lastest_comments=lastest_comments,
                multimedias=multimedias,
                league_id=LEAGUE_ID,
                category_id=category_id,
                api_domain=API_DOMAIN,
                category=category)

# 景区列表
class NewsupFranchisesHandler(BaseHandler):
    def get(self):
        logging.info(self.request)
        franchise_type = self.get_argument("franchise_type", "")
        logging.info("got franchise_type %r from argument", franchise_type)

        city = self.get_argument("city", "all")
        category = self.get_argument("category_id", "all")
        logging.info("got city %r from argument", city)
        logging.info("got category %r from argument", category)

        if isinstance(city, unicode):
            print city.encode('utf-8')
        else:
            print city.decode('utf-8').encode('utf-8')

        city = city.encode('utf-8')
        logging.info("got city %r encode utf-8", city)

        city = unquote(city)
        logging.info("got city %r unquote", city)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

        # league(联盟信息)
        league_info = self.get_league_info()

        # franchises(景区)
        params = {"franchise_type":franchise_type, "page":1, "limit":8}
        url = url_concat(API_DOMAIN+"/api/leagues/"+LEAGUE_ID+"/clubs-filter", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got franchises response %r", response.body)
        data = json_decode(response.body)
        franchises = data['rs']['data']

        # product(旅游产品)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"b0569f58144f11e78d3400163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got products response %r", response.body)
        data = json_decode(response.body)
        products = data['rs']
        for product in products:
            product['publish_time'] = timestamp_friendly_date(product['publish_time'])

        # journey(旅游资讯)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"065f565e6bd711e7b46300163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got journeies response %r", response.body)
        data = json_decode(response.body)
        journeies = data['rs']
        for article in journeies:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # communities(经验交流)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"1b86ad38f73411e69a3c00163e023e51", "idx":0, "limit":12}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        communities = data['rs']
        for article in communities:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # requires(景区需求/供应商需求)
        if franchise_type == '\xe6\x99\xaf\xe5\x8c\xba': #景区
            category_id = '065f565e6bd711e7b46300163e023e51'
        else:
            category_id = '404228663a1711e7b21000163e023e51'
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":category_id, "idx":0, "limit":12}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got requires response %r", response.body)
        data = json_decode(response.body)
        requires = data['rs']
        for article in requires:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # multimedia
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        multimedias = data['rs']
        for multimedia in multimedias:
            multimedia['publish_time'] = timestamp_friendly_date(multimedia['publish_time'])

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

        # tag
        hot_category_id = "757ee072a02511e7b7f600163e023e51"  #热门景区

        params = {"page":1, "limit":10}
        url = url_concat(API_DOMAIN+"/api/def/categories/"+ hot_category_id +"/level2", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        hot_tags = data['rs']

        recommend_category_id = "b1fb3e94a1e011e7943000163e023e51"  #推荐路线
        params = {"page":1, "limit":10}
        url = url_concat(API_DOMAIN+"/api/def/categories/"+ recommend_category_id +"/level2", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        recommend_tags = data['rs']

        recommend_category_id = "9a2f440eb96911e7a70e00163e023e51"  #旅游时长
        params = {"page":1, "limit":10}
        url = url_concat(API_DOMAIN+"/api/def/categories/"+ recommend_category_id +"/level2", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        duration_tags = data['rs']

        specialty_category_id = "0c511b26a1e011e7943000163e023e51"
        params = {"page":1, "limit":10}
        url = url_concat(API_DOMAIN+"/api/def/categories/"+ specialty_category_id +"/level2", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        specialty_tags = data['rs']

        self.render('newsup/new-franchises.html',
                league_info=league_info,
                is_login=is_login,
                is_ops=is_ops,
                city=city,
                category=category,
                franchises=franchises,
                requires=requires,
                products=products,
                journeies=journeies,
                communities=communities,
                multimedias=multimedias,
                lastest_comments=lastest_comments,
                league_id=LEAGUE_ID,
                api_domain=API_DOMAIN,
                franchise_type=franchise_type,
                hot_tags=hot_tags,
                recommend_tags=recommend_tags,
                duration_tags=duration_tags,
                specialty_tags=specialty_tags)


# 景区详情
class NewsupFranchiseDetailHandler(BaseHandler):
    def get(self):
        logging.info(self.request)
        franchise_id = self.get_argument("id", "")

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

        # league(联盟信息)
        league_info = self.get_league_info()

        # franchise
        params = {"filter":"detail"}
        url = url_concat(API_DOMAIN+"/api/clubs/"+franchise_id,params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got article response %r", response.body)
        data = json_decode(response.body)
        franchise = data['rs']
        geo_x = franchise['gcj02']['x']
        geo_y = franchise['gcj02']['y']
        if not franchise.has_key('paragraphs'):
            franchise['paragraphs'] = ''
        if not franchise.has_key('franchise_type'):
            franchise['franchise_type'] = 'franchise'
        if franchise.has_key('create_time'):
            franchise['create_time'] = timestamp_friendly_date(franchise['create_time'])
        else:
            franchise['create_time'] = timestamp_friendly_date(0)

        url = API_DOMAIN+"/api/clubs/"+franchise_id+"/car-parks"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        parkings = data['rs']
        for parking in parkings:
            parking['percent'] = int(float(parking['remain_space']) / float(parking['max_space'])*100)
            logging.info("got parking %r", parking['percent'])

        # update read_num
        read_num = franchise['read_num']
        url = API_DOMAIN+"/api/articles/"+franchise_id+"/read"
        http_client = HTTPClient()
        _body = {"read_num": read_num+1}
        _json = json_encode(_body)
        response = http_client.fetch(url, method="POST", body=_json)
        logging.info("got update read_num response %r", response.body)

        # product(旅游产品)
        # params = {"filter":"club", "club_id":franchise_id, "status":"publish", "category":"b0569f58144f11e78d3400163e023e51", "idx":0, "limit":4}
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"b0569f58144f11e78d3400163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        products = data['rs']
        for product in products:
            product['publish_time'] = timestamp_friendly_date(product['publish_time'])

        # journey(旅游资讯)
        # params = {"filter":"club", "club_id":franchise_id, "status":"publish", "category":"065f565e6bd711e7b46300163e023e51", "idx":0, "limit":4}
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"065f565e6bd711e7b46300163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        journeies = data['rs']
        for article in journeies:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # last_activity(近期活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        last_activities = data['rs']
        for article in last_activities:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # communities(经验交流)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"1b86ad38f73411e69a3c00163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        communities = data['rs']
        for article in communities:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # requires(景区需求)
        if franchise['franchise_type'] == '景区':
            category_id = '065f565e6bd711e7b46300163e023e51'
        else:
            category_id = '404228663a1711e7b21000163e023e51'
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":category_id, "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        requires = data['rs']
        for article in requires:
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
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        multimedias = data['rs']
        for multimedia in multimedias:
            multimedia['publish_time'] = timestamp_friendly_date(multimedia['publish_time'])

        self.render('newsup/franchise-detail.html',
                is_login=is_login,
                is_ops=is_ops,
                access_token=access_token,
                league_info=league_info,
                franchise=franchise,
                products=products,
                journeies=journeies,
                last_activities=last_activities,
                communities=communities,
                requires=requires,
                multimedias=multimedias,
                api_domain=API_DOMAIN,
                lastest_comments=lastest_comments,
                parkings=parkings,
                geo_x = geo_x,
                geo_y = geo_y)


# 供应商列表
class NewsupSuppliersHandler(BaseHandler):
    def get(self):
        logging.info(self.request)
        franchise_type = self.get_argument("franchise_type", "")
        logging.info("got franchise_type %r from argument", franchise_type)

        city = self.get_argument("city", "all")
        category = self.get_argument("category_id", "all")
        logging.info("got city %r from argument", city)
        logging.info("got category %r from argument", category)

        if isinstance(city, unicode):
            print city.encode('utf-8')
        else:
            print city.decode('utf-8').encode('utf-8')

        city = city.encode('utf-8')
        logging.info("got city %r encode utf-8", city)

        city = unquote(city)
        logging.info("got city %r unquote", city)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

        # league(联盟信息)
        league_info = self.get_league_info()

        # suppliers(供应商)
        params = {"franchise_type":franchise_type, "page":1, "limit":8}
        url = url_concat(API_DOMAIN+"/api/leagues/"+LEAGUE_ID+"/clubs-filter", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got franchises response %r", response.body)
        data = json_decode(response.body)
        suppliers = data['rs']['data']

        # product(特色产品)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"b0569f58144f11e78d3400163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got products response %r", response.body)
        data = json_decode(response.body)
        products = data['rs']
        for product in products:
            product['publish_time'] = timestamp_friendly_date(product['publish_time'])

        # journey(旅游资讯)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"065f565e6bd711e7b46300163e023e51", "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got journeies response %r", response.body)
        data = json_decode(response.body)
        journeies = data['rs']
        for article in journeies:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # communities(经验交流)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"1b86ad38f73411e69a3c00163e023e51", "idx":0, "limit":12}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        communities = data['rs']
        for article in communities:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # requires(景区需求/供应商需求)
        if franchise_type == '\xe6\x99\xaf\xe5\x8c\xba': #景区
            category_id = '065f565e6bd711e7b46300163e023e51'
        else:
            category_id = '404228663a1711e7b21000163e023e51'
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":category_id, "idx":0, "limit":12}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got requires response %r", response.body)
        data = json_decode(response.body)
        requires = data['rs']
        for article in requires:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # multimedia
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":4}
        url = url_concat(API_DOMAIN+"/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        multimedias = data['rs']
        for multimedia in multimedias:
            multimedia['publish_time'] = timestamp_friendly_date(multimedia['publish_time'])

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

        # tag
        hot_category_id = "8bc87862b98811e7805e00163e045306"  #特色产品

        params = {"page":1, "limit":10}
        url = url_concat(API_DOMAIN+"/api/def/categories/"+ hot_category_id +"/level2", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        hot_tags = data['rs']

        recommend_category_id = "b1fb3e94a1e011e7943000163e023e51"  #推荐路线
        params = {"page":1, "limit":10}
        url = url_concat(API_DOMAIN+"/api/def/categories/"+ recommend_category_id +"/level2", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        recommend_tags = data['rs']

        recommend_category_id = "9a2f440eb96911e7a70e00163e023e51"  #旅游时长
        params = {"page":1, "limit":10}
        url = url_concat(API_DOMAIN+"/api/def/categories/"+ recommend_category_id +"/level2", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        duration_tags = data['rs']

        specialty_category_id = "0c511b26a1e011e7943000163e023e51"
        params = {"page":1, "limit":10}
        url = url_concat(API_DOMAIN+"/api/def/categories/"+ specialty_category_id +"/level2", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        specialty_tags = data['rs']

        self.render('newsup/suppliers.html',
                league_info=league_info,
                is_login=is_login,
                is_ops=is_ops,
                city=city,
                category=category,
                suppliers=suppliers,
                requires=requires,
                products=products,
                journeies=journeies,
                communities=communities,
                multimedias=multimedias,
                lastest_comments=lastest_comments,
                league_id=LEAGUE_ID,
                api_domain=API_DOMAIN,
                franchise_type=franchise_type,
                hot_tags=hot_tags,
                recommend_tags=recommend_tags,
                duration_tags=duration_tags,
                specialty_tags=specialty_tags)


# 供应商详情
class NewsupSuppliersDetailHandler(BaseHandler):
    def get(self):
        logging.info(self.request)
        franchise_id = self.get_argument("id", "")

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

        # league(联盟信息)
        league_info = self.get_league_info()

        # franchise
        params = {"filter":"detail"}
        url = url_concat(API_DOMAIN+"/api/clubs/"+franchise_id,params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got article response %r", response.body)
        data = json_decode(response.body)
        franchise = data['rs']
        geo_x = franchise['gcj02']['x']
        geo_y = franchise['gcj02']['y']
        if not franchise.has_key('paragraphs'):
            franchise['paragraphs'] = ''
        if not franchise.has_key('franchise_type'):
            franchise['franchise_type'] = 'franchise'
        if franchise.has_key('create_time'):
            franchise['create_time'] = timestamp_friendly_date(franchise['create_time'])
        else:
            franchise['create_time'] = timestamp_friendly_date(0)

        url = API_DOMAIN+"/api/clubs/"+franchise_id+"/car-parks"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        parkings = data['rs']
        for parking in parkings:
            parking['percent'] = int(float(parking['remain_space']) / float(parking['max_space'])*100)
            logging.info("got parking %r", parking['percent'])

        # update read_num
        read_num = franchise['read_num']
        url = API_DOMAIN+"/api/articles/"+franchise_id+"/read"
        http_client = HTTPClient()
        _body = {"read_num": read_num+1}
        _json = json_encode(_body)
        response = http_client.fetch(url, method="POST", body=_json)
        logging.info("got update read_num response %r", response.body)

        # product(旅游产品)
        # params = {"filter":"club", "club_id":franchise_id, "status":"publish", "category":"b0569f58144f11e78d3400163e023e51", "idx":0, "limit":4}
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"b0569f58144f11e78d3400163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        products = data['rs']
        for product in products:
            product['publish_time'] = timestamp_friendly_date(product['publish_time'])

        # journey(旅游资讯)
        # params = {"filter":"club", "club_id":franchise_id, "status":"publish", "category":"065f565e6bd711e7b46300163e023e51", "idx":0, "limit":4}
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"065f565e6bd711e7b46300163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        journeies = data['rs']
        for article in journeies:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # last_activity(近期活动)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"0bbf89e2f73411e69a3c00163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        last_activities = data['rs']
        for article in last_activities:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # communities(经验交流)
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"1b86ad38f73411e69a3c00163e023e51", "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        communities = data['rs']
        for article in communities:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # requires(景区需求)
        if franchise['franchise_type'] == '景区':
            category_id = '065f565e6bd711e7b46300163e023e51'
        else:
            category_id = '404228663a1711e7b21000163e023e51'
        params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":category_id, "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        requires = data['rs']
        for article in requires:
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
        params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":10}
        url = url_concat(API_DOMAIN+"/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        multimedias = data['rs']
        for multimedia in multimedias:
            multimedia['publish_time'] = timestamp_friendly_date(multimedia['publish_time'])

        self.render('newsup/supplier-detail.html',
                is_login=is_login,
                is_ops=is_ops,
                access_token=access_token,
                league_info=league_info,
                franchise=franchise,
                products=products,
                journeies=journeies,
                last_activities=last_activities,
                communities=communities,
                requires=requires,
                multimedias=multimedias,
                api_domain=API_DOMAIN,
                lastest_comments=lastest_comments,
                parkings=parkings,
                geo_x = geo_x,
                geo_y = geo_y)


# 票列表
class NewsupTicketListHandler(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

        # league(联盟信息)
        league_info = self.get_league_info()
        club_id = self.get_argument('club_id','')
        logging.info('got club_id',club_id)

        params = {"filter":"club", "club_id":club_id, "page":1, "limit":5}
        url = url_concat(API_DOMAIN+"/api/items", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        tickets = data['rs']['data']

        self.render('newsup/ticket-list.html',
                is_login=is_login,
                is_ops=is_ops,
                club_id=club_id,
                league_info=league_info,
                access_token=access_token,
                api_domain=API_DOMAIN,
                tickets=tickets)


# 订票购物车
class NewsupTicketCartHandler(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        logging.info(self.request)
        ticket_id = self.get_argument("ticket_id",'')
        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

        # league(联盟信息)
        league_info = self.get_league_info()
        club_id = self.get_argument('club_id','')
        logging.info('got club_id',club_id)

        # 查询选择哪种票
        params = {"filter":"club", "club_id":club_id, "page":1, "limit":5}
        url = url_concat(API_DOMAIN+"/api/items", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        tickets = data['rs']['data']

        self.render('newsup/ticket-cart.html',
                is_login=is_login,
                is_ops=is_ops,
                club_id=club_id,
                league_info=league_info,
                access_token=access_token,
                api_domain=API_DOMAIN,
                ticket_id=ticket_id,
                tickets=tickets)

    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):
        club_id = self.get_argument('club_id','')
        logging.info('got club_id',club_id)

        access_token = self.get_secure_cookie("access_token")
        #购物车商品json
        items = self.get_body_argument("items", [])
        logging.info("got items %r", items)
        items = JSON.loads(items)
        logging.info("got items %r", items)

        item_id = "00000000000000000000000000000000"
        _timestamp = int(time.time())

        #订票人信息
        addr = self.get_argument("addr_input", {})
        logging.info("got addr %r", addr)
        addr = JSON.loads(addr)
        logging.info("got addr %r", addr)

        # 游玩日期
        play_time = self.get_argument('play-time','')
        logging.info('got play_time',play_time)
        play_time = date_timestamp(play_time)

        order_id = str(uuid.uuid1()).replace('-', '')
        # 创建订单索引
        order_index = {
            "_id": order_id,
            "order_type": "buy_item",
            "club_id": club_id,
            "item_type": "items",
            "item_id": item_id,
            "item_name": "", # 由服务器端填写第一个商品名称
            "distributor_type": "item",
            "items":items,
            "shipping_addr":addr,
            "shipping_cost":0, # 由服务器端计算运费
            "billing_required":0,
            "distributor_id": "00000000000000000000000000000000",
            "create_time": _timestamp,
            "pay_type": "wxpay",
            "pay_status": 10,
            "quantity": 0, # 由服务器端计算商品数量
            "amount": 0, # 由服务器端计算商品合计
            "actual_payment": 0, # 由服务器端计算实际支付金额
            "base_fees": [], #基本服务
            "ext_fees": [], # 附加服务项编号数组
            "insurances": [], # 保险选项,数组
            "vouchers": [], #代金券选项,数组
            "points_used": 0, # 使用积分数量
            "bonus_points": 0, # 购买商品获得奖励积分
            "booking_time": play_time,
        }
        pay_id = self.create_order(order_index)

        # 清空购物车
        headers = {"Authorization":"Bearer "+access_token}
        url = API_DOMAIN + "/api/clubs/"+ club_id +"/cart/items"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="DELETE", headers=headers)
        logging.info("update item response.body=[%r]", response.body)

        self.redirect("/portal/newsup/pay-style?club_id="+club_id+"&order_id="+order_id)


# 订票结算页
class NewsupTicketBalanceHandler(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

        # league(联盟信息)
        league_info = self.get_league_info()
        club_id = self.get_argument('club_id','')
        logging.info('got club_id',club_id)
        order_id = self.get_argument('order_id','')
        logging.info('got order_id',order_id)

        order = self.get_symbol_object(order_id)
        logging.info("GET order %r", order)
        order['create_time'] = timestamp_datetime(float(order['create_time']))

        items = order['items']
        _product_description = items[0]['title']
        logging.info("GET items %r", items)

        self.render('newsup/pay-style.html',
                is_login=is_login,
                is_ops=is_ops,
                club_id=club_id,
                league_info=league_info,
                access_token=access_token,
                api_domain=API_DOMAIN,
                order = order,
                items=items)


# 订单列表页
class NewsupOrderListHandler(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

        # league(联盟信息)
        league_info = self.get_league_info()
        club_id = self.get_argument('club_id','')
        logging.info('got club_id',club_id)
        order_id = self.get_argument('order_id','')
        logging.info('got order_id',order_id)

        order = self.get_order_index(order_id)
        logging.info("GET order %r", order)
        order['create_time'] = timestamp_datetime(float(order['create_time']))

        items = order['items']
        _product_description = items[0]['title']
        logging.info("GET items %r", items)

        self.render('newsup/order-list.html',
                is_login=is_login,
                is_ops=is_ops,
                club_id=club_id,
                league_info=league_info,
                access_token=access_token,
                api_domain=API_DOMAIN,
                order = order)


class NewsupApplyFranchiseHandler(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

        # league(联盟信息)
        league_info = self.get_league_info()

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
                is_ops=is_ops,
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

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        is_ops = False
        if is_login:
            is_ops = self.is_ops(access_token)

        # league(联盟信息)
        league_info = self.get_league_info()

        # product(旅游产品)
        # params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"b0569f58144f11e78d3400163e023e51", "idx":0, "limit":4}
        # url = url_concat(API_DOMAIN+"/api/articles", params)
        # http_client = HTTPClient()
        # response = http_client.fetch(url, method="GET")
        # logging.info("got response %r", response.body)
        # data = json_decode(response.body)
        # products = data['rs']
        # for product in products:
        #     product['publish_time'] = timestamp_friendly_date(product['publish_time'])
        #
        # # journey(旅游资讯)
        # params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"065f565e6bd711e7b46300163e023e51", "idx":0, "limit":4}
        # url = url_concat(API_DOMAIN+"/api/articles", params)
        # http_client = HTTPClient()
        # response = http_client.fetch(url, method="GET")
        # logging.info("got response %r", response.body)
        # data = json_decode(response.body)
        # journeies = data['rs']
        # for article in journeies:
        #     article['publish_time'] = timestamp_friendly_date(article['publish_time'])
        #
        # # communities(经验交流)
        # params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":"1b86ad38f73411e69a3c00163e023e51", "idx":0, "limit":12}
        # url = url_concat(API_DOMAIN+"/api/articles", params)
        # http_client = HTTPClient()
        # response = http_client.fetch(url, method="GET")
        # logging.info("got response %r", response.body)
        # data = json_decode(response.body)
        # communities = data['rs']
        # for article in communities:
        #     article['publish_time'] = timestamp_friendly_date(article['publish_time'])
        #
        # # requires(景区需求)
        # params = {"filter":"league", "league_id":LEAGUE_ID, "status":"publish", "category":'065f565e6bd711e7b46300163e023e51', "idx":0, "limit":12}
        # url = url_concat(API_DOMAIN+"/api/articles", params)
        # http_client = HTTPClient()
        # response = http_client.fetch(url, method="GET")
        # logging.info("got response %r", response.body)
        # data = json_decode(response.body)
        # requires = data['rs']
        # for article in requires:
        #     article['publish_time'] = timestamp_friendly_date(article['publish_time'])
        #
        # # multimedia
        # params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":4}
        # url = url_concat(API_DOMAIN+"/api/multimedias", params)
        # http_client = HTTPClient()
        # response = http_client.fetch(url, method="GET")
        # logging.info("got response %r", response.body)
        # data = json_decode(response.body)
        # multimedias = data['rs']
        # for multimedia in multimedias:
        #     multimedia['publish_time'] = timestamp_friendly_date(multimedia['publish_time'])
        #
        # # lastest comments(最新的评论)
        # params = {"filter":"league", "league_id":LEAGUE_ID, "idx":0, "limit":5}
        # url = url_concat(API_DOMAIN+"/api/last-comments", params)
        # http_client = HTTPClient()
        # response = http_client.fetch(url, method="GET")
        # logging.info("got response %r", response.body)
        # data = json_decode(response.body)
        # lastest_comments = data['rs']
        # for comment in lastest_comments:
        #     comment['create_time'] = timestamp_friendly_date(comment['create_time'])

        self.render('newsup/search-result.html',
                is_login=is_login,
                is_ops=is_ops,
                league_info=league_info,
                league_id=LEAGUE_ID,
                api_domain=API_DOMAIN)


# ajax 访问数据API
class ApiArticlesXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, vendor_id):
        logging.info("got vendor_id %r in uri", vendor_id)
        category_id = self.get_argument("category", "")
        logging.debug("get category_id=[%r]", category_id)
        page = self.get_argument("page", 1)
        logging.debug("get page=[%r] from argument", page)
        limit = self.get_argument("limit", 20)
        logging.debug("get limit=[%r] from argument", limit)

        access_token = self.get_access_token()

        params = {"filter":league, "league_id":LEAGUE_ID, "status":"publish","category":category_id, "page":page, "limit":limit}
        url = url_concat(API_DOMAIN + "/api/articles-pagination", params)
        http_client = HTTPClient()
        headers = {"Authorization":"Bearer " + access_token}
        response = http_client.fetch(url, method="GET", headers=headers)
        logging.info("got response.body %r", response.body)
        data = json_decode(response.body)
        rs = data['rs']
        articles = rs['data']

        for article in articles:
            # 下单时间，timestamp -> %m月%d 星期%w
            article['create_time'] = timestamp_datetime(float(article['create_time']))

        self.write(JSON.dumps(rs, default=json_util.default))
        self.finish()
