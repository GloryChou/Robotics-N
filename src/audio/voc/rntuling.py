# -*- coding: utf-8 -*-
import urllib, urllib2, pycurl
import json

class Rntuling(object):

    def __init__(self):
        key = '04a8d8336095b40fa8b4898a8ed87e8c'
        self.__apiurl = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='

    def Get_response(self, info):
        request = self.__apiurl + info
        # 发出http请求
        page = urllib.urlopen(request)
        html = page.read()
        resJson = json.loads(html)  # 返回结果(JSON格式)
        response = resJson['text']
        return response