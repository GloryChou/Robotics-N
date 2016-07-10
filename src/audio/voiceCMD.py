# -*- coding: utf-8 -*-
from rnaudio import *
from bdasr import *
from rntuling import *

# 检测语音内容是否为命令
def checkcmd(text):
    

# 语音控制流程
if __name__ = '__main__':
    rna = Rnaudio()     # 音频控制模块
    asr = BDasr()       # 语音识别模块
    rnt = Rntuling()    # 对话模块

    print "******开启语音控制******"
    while True:
        # 录音
        filename = rna.Record()

        if(filename != ""):
            # 识别录音内容
            text = asr.Recognise(filename)

            # 如果不是命令，则进行对话
            if(!checkcmd(text)):
                # 与图灵机器人对话
                response = rnt.Get_response(text)
                print response
            else: # 若是命令，执行机械操作
                

    print "******结束语音控制******"

