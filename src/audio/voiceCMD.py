# -*- coding: utf-8 -*-
import sys
sys.path.append("./voc")

from rnaudio import *
from bdasr import *
from rntuling import *

CMD_LST = ["前进","后退","左转","右转","停止"]

# 检测语音内容是否为命令
def checkCmd(text):
    if(CMD_LST.index(text) < 0):
        return False
    return True

# 执行命令
def exeCmd(cmd):
    if(CMD_LST.index(text) == 0):
        # 前进
    elif(CMD_LST.index(text) == 1):
        # 后退
    elif(CMD_LST.index(text) == 2):
        # 左转
    elif(CMD_LST.index(text) == 3):
        # 右转
    else:
        # 停止

# 语音控制流程
if __name__ == '__main__':
    rna = Rnaudio()     # 音频控制模块
    asr = BDasr()       # 语音识别模块
    rnt = Rntuling()    # 对话模块

    print "******开启语音控制******"
    while True:
        # 录音，并获取录音文件
        rcd_filename = rna.Record()

        if(rcd_filename != ""):
            # 识别录音内容
            text = asr.Recognise(rcd_filename)
            # 删除录音文件
            rna.Delete(rcd_filename)
            # 如果不是命令，则进行对话
            if(!checkCmd(text)):
                # 与图灵机器人对话，获取回复内容
                response = rnt.Get_response(text)
                print response
                # 语音合成，并获取合成的语音文件
                cps_filename = asr.Compose(response)
                # 播放语音
                rna.Play_MP3(cps_filename)
                # 删除合成的语音文件
                rna.Delete(cps_filename)
            else: # 若是命令，执行机械操作
                exeCmd(text)
    print "******结束语音控制******"

