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

from comm import cur_file_dir
from comm import timestamp_date


class UicnIndexHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        self.render('uicn/index.html')

class UicnListHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        self.render('uicn/list.html')

class UicnExpHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        self.render('uicn/exp.html')

class UicnBookHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        self.render('uicn/book.html')

class UicnStudyHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        self.render('uicn/study.html')

class UicnGameHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        self.render('uicn/game.html')

class UicnPeixunHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        self.render('uicn/peixun.html')

class UicnTopicHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        self.render('uicn/topic.html')

class UicnOnlineHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        self.render('uicn/online.html')

class UicnZhaopinHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        self.render('uicn/zhaopin.html')

# 登录 注册 找回handler
class AuthLoginHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        self.render('auth/login.html')

class AuthGetpassHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        self.render('auth/getpass.html')

class AuthRegHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        self.render('auth/reg.html')

class AuthFindpassHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        self.render('auth/findpassbymail.html')

class AuthChangepassHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        self.render('auth/changepass.html')

class AuthEditsuccessHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        self.render('auth/editsuccess.html')
