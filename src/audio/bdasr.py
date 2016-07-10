# -*- coding: utf-8 -*-
import os
import urllib, urllib2, pycurl
import wave
from datetime import datetime
import numpy as np
import json

VOICECONTENT = ""

# 百度语音识别操作类
class BDasr(object):

    def __init__(self):
        # 初始化访问参数
        apiKey = "y6NojQriI2VR9xakcoaE9CUU"
        secretKey = "a54d9ff9738361fcb6137f7bd3dfd7cb"
        auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey;

        # 获取访问百度API的token
        res = urllib2.urlopen(auth_url)
        json_data = res.read()
        self.__access_token = json.loads(json_data)['access_token']

        '''************** <API相关配置> **************'''
        self.__cuid = "8235048"         # 用户标识，要求填写唯一确定用户的代号，我这里填写的是产品id
        '''************** </API相关配置> **************'''

    @property
    def access_token(self):
        return self.__access_token

    @property
    def cuid(self):
        return self.__cuid
    @cuid.setter
    def cuid(self, cuid):
        self.__cuid = cuid

    # 语音识别
    def Recognise(self, filename):

        # 上传音频文件参数、URL
        fp = wave.open(filename, 'rb')
        np = fp.getnframes()
        f_len = nf * 2
        audio_data = fp.readframes(nf)
        
        srv_url = 'http://vop.baidu.com/server_api?lan=zh&cuid=' + self.cuid + '&token=' + self.access_token
        http_header = [
            'Content-Type: audio/pcm; rate=8000',
            'Content-Length: %d' % f_len
        ]

        # url
        c = pycurl.Curl()
        c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode
        c.setopt(c.HTTPHEADER, http_header)   #must be list, not dict
        c.setopt(c.POST, 1)
        c.setopt(c.CONNECTTIMEOUT, 30)
        c.setopt(c.TIMEOUT, 30)
        c.setopt(c.POSTFIELDS, audio_data)
        c.setopt(c.POSTFIELDSIZE, f_len)
        c.setopt(c.WRITEFUNCTION, self.__Dump_res)
        c.perform()

    def __Dump_res(self, buf):
        global VOICECONTENT
        print buf
        res = eval(buf)   # 返回结果(jsno格式)
        print type(res)
        if res['err_msg'] == 'success.':
            VOICECONTENT = res['result'][0]
            print VOICECONTENT

    # 语音合成
    def Compose(self, text):
        # 字符串转成编码
        text = urllib2.quote(text)
        # 语音合成URL
        srv_url = 'http://tsn.baidu.com/text2audio?lan=zh&ctp=1&cuid=' + self.cuid + '&tok=' + self.access_token + '&tex=' + text
        # 由百度TTS生成语音，获取音频的二进制流
        data  = urllib2.urlopen(srv_url)
        
        # 生成本地音频文件
        cfilename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + "_Compose.mp3"
        '''wf = wave.open(cfilename, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(8000)
        wf.writeframes(data.read())'''
        f_output = open(cfilename, "wb")
        f_output.write(data.read())
        return cfilename        

