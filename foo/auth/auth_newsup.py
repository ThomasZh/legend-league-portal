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


class AuthRegisterHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True

        self.render('newsup/register.html',
                is_login=is_login)


class AuthLogoutHandler(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        access_token = self.get_secure_cookie("access_token")

        # logout
        url = "http://api.7x24hs.com/api/auth/tokens"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="DELETE", headers={"Authorization":"Bearer "+access_token})
        logging.info("got response %r", response.body)
        self.clear_cookie("access_token")
        self.clear_cookie("expires_at")
        self.clear_cookie("login_next")
        self.clear_cookie("refresh_token")

        self.redirect("/");


class AuthLeagueSignupXHR(BaseHandler):
    def post(self):
        logging.info(self.request)
        logging.info(self.request.body)
        session_ticket = json_decode(self.request.body)

        self.set_secure_cookie("access_token", session_ticket['access_token'])
        self.set_secure_cookie("expires_at", str(session_ticket['expires_at']))

        # signup into league
        url = "http://api.7x24hs.com/api/leagues/"+LEAGUE_ID+"/signup"
        http_client = HTTPClient()
        headers={"Authorization":"Bearer "+session_ticket['access_token']}
        body = {"role":"user"}
        _json = json_encode(body)
        response = http_client.fetch(url, method="POST", headers=headers, body=_json)
        logging.info("got response %r", response.body)

        self.set_status(200) # OK
        self.finish()
        return
