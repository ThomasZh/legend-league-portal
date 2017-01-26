#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2016 7x24hs.com
# thomas@7x24hs.com
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
import hashlib
import json as JSON # 启用别名，不会跟方法里的局部变量混淆
from bson import json_util
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../dao"))

from tornado.escape import json_encode, json_decode
from tornado.httpclient import *
from tornado.httputil import url_concat
from bson import json_util

from comm import *
from global_const import *


class AuthEmailLoginHandler(BaseHandler):
    def get(self):
        logging.info(self.request)
        err_msg = ""
        self.render('auth/email-login.html', err_msg=err_msg)


class AuthEmailRegisterHandler(BaseHandler):
    def get(self):
        err_msg = ""
        self.render('auth/email-register.html', err_msg=err_msg)


class AuthEmailForgotPwdHandler(BaseHandler):
    def get(self):
        err_msg = "When you fill in your registered email address, you will be sent instructions on how to reset your password."
        self.render('auth/email-forgot-pwd.html', err_msg=err_msg)


class AuthEmailResetPwdHandler(BaseHandler):
    def get(self):
        logging.info(self.request)
        ekey = self.get_argument("ekey", "")
        email = self.get_argument("email", "")
        logging.info("try reset email=[%r] password by ekey=[%r]", email, ekey)

        err_msg = ""
        self.render('auth/email-reset-pwd.html',
                err_msg=err_msg,
                email=email,
                ekey=ekey)


class AuthWelcomeHandler(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        self.render('auth/welcome.html')


class AuthLogoutHandler(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):
        access_token = self.get_secure_cookie("access_token")

        # logout
        url = "http://api.7x24hs.com/auth/token"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="DELETE", headers={"Authorization":"Bearer "+access_token})
        logging.info("got response %r", response.body)
        self.clear_cookie("access_token")
        self.clear_cookie("expires_at")

        self.redirect("/");
