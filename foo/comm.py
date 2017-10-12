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
import random
import hashlib
from hashlib import md5
import string
import json as JSON # 启用别名，不会跟方法里的局部变量混淆
from bson import json_util
from tornado.escape import json_encode, json_decode
from tornado.httpclient import *
from tornado.httputil import url_concat

from global_const import *


class singleton(object):
    _singleton = None;
    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = object.__new__(cls);
        return cls._singleton;


#获取脚本文件的当前路径
def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)


# 时间格式转换
def timestamp_date(value):
    #_format = '%Y-%m-%d %H:%M:%S'
    _format = '%Y/%m/%d/%H'
    # value is timestamp(int), eg: 1332888820
    _value = time.localtime(value)
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    _dt = time.strftime(_format, _value)
    return _dt


def timestamp_friendly_date(value):
    #_format = '%Y-%m-%d %H:%M:%S'
    y_format = '%Y'
    m_format = '%m'
    d_format = '%d'
    w_format = '%w'
    # value is timestamp(int), eg: 1332888820
    _value = time.localtime(value)
    _current = time.localtime()
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    current_y_dt = time.strftime(y_format, _current)
    y_dt = time.strftime(y_format, _value)
    m_dt = time.strftime(m_format, _value)
    d_dt = time.strftime(d_format, _value)
    w_dt = time.strftime(w_format, _value)
    if w_dt == '0':
        if current_y_dt == y_dt:
            _dt = str(int(m_dt)) + '月' + str(int(d_dt)) + ' 星期日'
        else:
            _dt = str(int(y_dt)) + '年' + str(int(m_dt)) + '月' + str(int(d_dt)) + ' 星期日'
    elif w_dt == '1':
        if current_y_dt == y_dt:
            _dt = str(int(m_dt)) + '月' + str(int(d_dt)) + ' 星期一'
        else:
            _dt = str(int(y_dt)) + '年' + str(int(m_dt)) + '月' + str(int(d_dt)) + ' 星期一'
    elif w_dt == '2':
        if current_y_dt == y_dt:
            _dt = str(int(m_dt)) + '月' + str(int(d_dt)) + ' 星期二'
        else:
            _dt = str(int(y_dt)) + '年' + str(int(m_dt)) + '月' + str(int(d_dt)) + ' 星期二'
    elif w_dt == '3':
        if current_y_dt == y_dt:
            _dt = str(int(m_dt)) + '月' + str(int(d_dt)) + ' 星期三'
        else:
            _dt = str(int(y_dt)) + '年' + str(int(m_dt)) + '月' + str(int(d_dt)) + ' 星期三'
    elif w_dt == '4':
        if current_y_dt == y_dt:
            _dt = str(int(m_dt)) + '月' + str(int(d_dt)) + ' 星期四'
        else:
            _dt = str(int(y_dt)) + '年' + str(int(m_dt)) + '月' + str(int(d_dt)) + ' 星期四'
    elif w_dt == '5':
        if current_y_dt == y_dt:
            _dt = str(int(m_dt)) + '月' + str(int(d_dt)) + ' 星期五'
        else:
            _dt = str(int(y_dt)) + '年' + str(int(m_dt)) + '月' + str(int(d_dt)) + ' 星期五'
    elif w_dt == '6':
        if current_y_dt == y_dt:
            _dt = str(int(m_dt)) + '月' + str(int(d_dt)) + ' 星期六'
        else:
            _dt = str(int(y_dt)) + '年' + str(int(m_dt)) + '月' + str(int(d_dt)) + ' 星期六'
    return _dt


def timestamp_datetime(value):
    #_format = '%Y-%m-%d %H:%M:%S'
    _format = '%m/%d/%Y %H:%M'
    # value is timestamp(int), eg: 1332888820
    _value = time.localtime(value)
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    _dt = time.strftime(_format, _value)
    return _dt


def date_timestamp(dt):
     # dt is string
     time.strptime(dt, '%Y-%m-%d')
     ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
     # "2012-03-28 06:53:40" to timestamp(int)
     _timestamp = time.mktime(time.strptime(dt, '%Y-%m-%d'))
     return int(_timestamp)


def datetime_timestamp(dt):
     # dt is string
     time.strptime(dt, '%m/%d/%Y %H:%M')
     ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
     # "2012-03-28 06:53:40" to timestamp(int)
     _timestamp = time.mktime(time.strptime(dt, '%m/%d/%Y %H:%M'))
     return int(_timestamp)


def generate_md5(fp):
    m = md5()
    m.update(fp)
    return m.hexdigest()


# 创建发生短信的 sendcloud 签名
def generate_sms_sign(SMS_KEY, param):
    param_keys = list(param.keys())
    param_keys.sort()

    param_str = ""
    for key in param_keys:
        param_str += key + '=' + str(param[key]) + '&'
    param_str = param_str[:-1]

    sign_str = SMS_KEY + '&' + param_str + '&' + SMS_KEY
    #sign = generate_md5(sign_str)
    sign = hashlib.md5(sign_str).hexdigest()

    return sign


# 生成4位数字验证码
def generate_verify_code():
    chars=['0','1','2','3','4','5','6','7','8','9']
    x = random.choice(chars),random.choice(chars),random.choice(chars),random.choice(chars)
    verifyCode = "".join(x)
    return verifyCode


#验证码函数
def randon_x(i):
    code = []
    for i in range(i):
        if i == random.randint(1,3):
            code.append(str(random.randint(1,9)))
        else:
            tmp = random.randint(65,90)
            code.append(chr(tmp))

    return ''.join(code)


def generate_uuid_str():
    return str(uuid.uuid1()).replace('-', '')


def generate_nonce_str():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))


def hash_pwd(md5pwd, salt):
    md5salt = hashlib.md5(salt).hexdigest()
    ecrypted_pwd = hashlib.md5(md5pwd + md5salt).hexdigest()
    return ecrypted_pwd


class PageNotFoundHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('comm/page-404.html')


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("pragma","no-cache")
        self.set_header("Cache-Control","no-store")
        self.set_header("Cache-Control","no-cache")
        self.set_header("expires","0")

    def get_league_info(self):
        # league(联盟信息)
        url = API_DOMAIN+"/api/leagues/"+LEAGUE_ID
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        league_info = data['rs']
        return league_info


    def get_code(self):
        url = API_DOMAIN+"/api/auth/codes"
        http_client = HTTPClient()
        data = {"appid":"7x24hs:blog",
                "app_secret":"2518e11b3bc89ebec594350d5739f29e"}
        _json = json_encode(data)
        response = http_client.fetch(url, method="POST", body=_json)
        session_code = json_decode(response.body)
        logging.info("got session_code %r", session_code)
        code = session_code['code']
        return code

    def write_error(self, status_code, **kwargs):
        host = self.request.headers['Host']
        logging.info("got host %r", host)

        try:
            reason = ""
            for line in traceback.format_exception(*kwargs["exc_info"]):
                if "HTTP 404: Not Found" in line:
                    self.render('comm/page-404.html')
                    self.finish()
                reason += line
            logging.info("got status_code %r reason %r", status_code, reason)

            params = {"app":"club-ops", "sys":host, "level":status_code, "message": reason}
            url = url_concat("http://kit.7x24hs.com/api/sys-error", params)
            http_client = HTTPClient()
            _json = json_encode(params)
            response = http_client.fetch(url, method="POST", body=_json)
            logging.info("got response.body %r", response.body)
        except:
            logging.warn("write log to http://kit.7x24hs.com/api/sys-error error")

        self.render("comm/page-500.html",
                status_code=status_code)


    def is_ops(self, access_token):
        try:
            params = {"filter":"ops"}
            url = url_concat(API_DOMAIN+"/api/myinfo", params)
            http_client = HTTPClient()
            headers={"Authorization":"Bearer "+access_token}
            response = http_client.fetch(url, method="GET", headers=headers)
            logging.info("got response %r", response.body)
            # account_id,nickname,avatar,club_id,club_name,league_id,_rank
            data = json_decode(response.body)
            ops = data['rs']
            return True
        except:
            err_title = str( sys.exc_info()[0] );
            err_detail = str( sys.exc_info()[1] );
            logging.error("error: %r info: %r", err_title, err_detail)
            return False


class AuthorizationHandler(BaseHandler):
    def get_current_user(self):
        self.set_secure_cookie("login_next", self.request.uri)

        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token %r from cookie", access_token)
        if not access_token:
            return None
        else:
            expires_at = self.get_secure_cookie("expires_at")
            logging.info("got expires_at %r from cookie", expires_at)
            if not expires_at:
                return None
            else:
                _timestamp = int(time.time())
                if int(expires_at) > _timestamp:
                    return access_token
                else:
                    # Logic: refresh_token
                    refresh_token = self.get_secure_cookie("refresh_token")
                    if not refresh_token:
                        return None
                    else:
                        try:
                            url = API_DOMAIN+"/api/auth/tokens"
                            http_client = HTTPClient()
                            headers={"Authorization":"Bearer "+refresh_token}
                            data = {"action":"refresh"}
                            _json = json_encode(data)
                            logging.info("request %r body %r", url, _json)
                            response = http_client.fetch(url, method="POST", headers=headers, body=_json)
                            logging.info("got response %r", response.body)
                            session_ticket = json_decode(response.body)

                            self.set_secure_cookie("access_token", session_ticket['access_token'])
                            self.set_secure_cookie("expires_at", str(session_ticket['expires_at']))
                            self.set_secure_cookie("refresh_token", session_ticket['refresh_token'])
                            return session_ticket['access_token']
                        except:
                            return None
                    return None


    def create_order(self, order_index):
        access_token = self.get_access_token()
        headers = {"Authorization":"Bearer "+access_token}

        url = API_DOMAIN + "/api/orders"
        http_client = HTTPClient()
        _json = json_encode(order_index)
        response = http_client.fetch(url, method="POST", headers=headers, body=_json)
        logging.info("create order=[%r] response=[%r]", order_index, response.body)
        data = json_decode(response.body)
        rs = data['rs']
        return rs['pay_id']


    def get_access_token(self):
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            logging.info("got access_token=[%r] from cookie", access_token)
        else:
            try:
                access_token = self.request.headers['Authorization']
                access_token = access_token.replace('Bearer ','')
            except:
                logging.warn("got access_token=[null] from headers")
                self.set_status(401) # Unauthorized
                self.write('Unauthorized')
                self.finish()
                return
            logging.info("got access_token=[%r] from headers", access_token)
        return access_token


    def get_symbol_object(self, _id):
        url = API_DOMAIN + "/api/symbols/" + _id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got symbol_object=[%r]", response.body)
        data = json_decode(response.body)
        if data['err_code'] == 404:
            return None
        symbol_object = data['rs']
        return symbol_object


    def get_order_index(self, order_id):
        headers = {"Authorization":"Bearer "+"00000000000000000000000000000000"}

        url = API_DOMAIN + "/api/orders/" + order_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET", headers=headers)
        logging.info("got order_index response.body=[%r]", response.body)
        data = json_decode(response.body)
        if data['err_code'] == 404:
            return None
        return data['rs']
