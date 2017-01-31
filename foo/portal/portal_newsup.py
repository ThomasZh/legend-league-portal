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

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/index.html',
                is_login=is_login)


class NewsupAccountHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/account.html',
                is_login=is_login)


class NewsupAuthorHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/author.html',
                is_login=is_login)


class NewsupMediaHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/media.html',
                is_login=is_login)


class NewsupShortcodesHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/shortcodes.html',
                is_login=is_login)


class NewsupContactHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/contact.html',
                is_login=is_login)


class NewsupItemDetailHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/item-detail.html',
                is_login=is_login)


class NewsupNewHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/new.html',
                is_login=is_login)


class NewsupCategoryHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/category.html',
                is_login=is_login)


class NewsupFranchiseHandler(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/franchise.html',
                is_login=is_login)
