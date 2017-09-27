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


class AuthRegisterHandler(BaseHandler):
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True
        is_ops = False

        # league(联盟信息)
        league_info = self.get_league_info()

        self.render('newsup/register.html',
                is_login=is_login,
                is_ops=is_ops,
                league_info=league_info,
                api_domain=API_DOMAIN)


class AuthLoginHandler(BaseHandler):
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True
        is_ops = False

        # league(联盟信息)
        league_info = self.get_league_info()

        self.render('newsup/login.html',
                is_login=is_login,
                is_ops=is_ops,
                league_info=league_info,
                api_domain=API_DOMAIN)


class AuthLostpwdHandler(BaseHandler):
    def get(self):
        logging.info(self.request)

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            is_login = True
        is_ops = False

        # league(联盟信息)
        league_info = self.get_league_info()

        self.render('newsup/lost-pwd.html',
                is_login=is_login,
                is_ops=is_ops,
                league_info=league_info,
                api_domain=API_DOMAIN)

# class AuthLogoutHandler(AuthorizationHandler):
    # @tornado.web.authenticated  # if no session, redirect to login page
class AuthLogoutHandler(BaseHandler):
    def get(self):
        logging.info("^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^")
        logging.info("^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^")
        logging.info("GET %r", self.request.uri)

        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token=[%r]", access_token)

        # logout
        url = API_DOMAIN+"/api/auth/tokens"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="DELETE", headers={"Authorization":"Bearer "+access_token})
        logging.info("got logout response %r", response.body)
        self.set_secure_cookie("access_token", "")
        self.set_secure_cookie("expires_at", "")
        self.set_secure_cookie("login_next", "")
        self.set_secure_cookie("refresh_token", "")
        self.clear_cookie("access_token")
        self.clear_cookie("expires_at")
        self.clear_cookie("login_next")
        self.clear_cookie("refresh_token")
        logging.info("clear cookie [access_token,expires_at,login_next,refresh_token]")

        logging.info("OK(200): logout success")
        logging.info("~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~")
        logging.info("~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~")

        self.redirect("/");


class AuthLeagueSignupXHR(BaseHandler):
    def post(self):
        logging.info("^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^")
        logging.info("^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^ ^^^^^")
        logging.info("POST %r", self.request.uri)
        logging.info(self.request.body)

        session_ticket = json_decode(self.request.body)
        self.set_secure_cookie("access_token", session_ticket['access_token'])
        self.set_secure_cookie("expires_at", str(session_ticket['expires_at']))

        # signup into league
        url = API_DOMAIN+"/api/leagues/"+LEAGUE_ID+"/signup"
        http_client = HTTPClient()
        headers={"Authorization":"Bearer "+session_ticket['access_token']}
        body = {"role":"user"}
        _json = json_encode(body)
        response = http_client.fetch(url, method="POST", headers=headers, body=_json)
        logging.info("got response %r", response.body)

        logging.info("OK(200): league-signup success session_ticket=[%r]", session_ticket)
        logging.info("~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~")
        logging.info("~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~")

        self.set_status(200) # OK
        self.write(JSON.dumps({"err_code":200, "err_msg":"success"}))
        self.finish()
        return
