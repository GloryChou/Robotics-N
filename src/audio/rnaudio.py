# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
import wave
import numpy as np 
from datetime import datetime 
import traceback

rnfilename = ""

class Rnaudio(object):

    # 初始化：类似于构造函数
    def __init__(self, cacheblock_size=2000, sampling_rate=8000, level=10000, sampling_num=20, max_silence_length=4):
        self.__cacheblock_size = cacheblock_size
        self.__sampling_rate = sampling_rate
        self.__level = level
        self.__sampling_num = sampling_num
        self.__max_silence_length = max_silence_length
    
    # 私有变量的getter、setter
    # cacheblock_size：pyAudio内部缓存的块的大小
    @property
    def cacheblock_size(self):
        return self.__cacheblock_size
    @cacheblock_size.setter
    def cacheblock_size(self, cbsize):
        self.__cacheblock_size = cbsize

    # sampling_rate：取样频率
    @property
    def sampling_rate(self):
        return self.__sampling_rate
    @sampling_rate.setter
    def sampling_rate(self, sprate):
        self.__sampling_rate = sprate
    
    # level：声音保存的阈值，超过这个阈值的样本即为取样成功的样本
    @property
    def level(self):
        return self.__level
    @level.setter
    def level(self, level):
        self.__level = level

    # sampling_num：取样个数，表示达到写入音频文件要求的最少的取样成功的样本个数
    @property
    def sampling_num(self):
        return self.__sampling_num
    @sampling_num.setter
    def sampling_num(self, snum):
        self.__sampling_num = snum
    
    # max_silence_length：记录长度
    @property
    def max_silence_length(self):
        return self.__max_silence_length
    @max_silence_length.setter
    def max_silence_length(self, rlen):
        self.__max_silence_length = rlen

    # 私有函数：将data中的数据保存到名为FILENAME的WAV文件中
    def __Save_wave_file(self, filename, data):
        wf = wave.open(filename, 'wb')
        # 配置声道数、量化位数和取样频率
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(self.sampling_rate)
        wf.writeframes("".join(data))
        wf.close()

    # 公有函数：开始录音-->存储录音文件-->返回录音文件名
    def Record(self):
        # 开启声音输入
        pa = PyAudio()

        stream = pa.open(format=paInt16, channels=1, rate=self.sampling_rate, input=True, 
                        frames_per_buffer=self.cacheblock_size)

        silence_count = 0       # 一次失败的取样记数成一次静音数
        save_buffer = []        # 音频缓冲

        try:
            while True:
                # 录音、取样
                string_audio_data = stream.read(self.cacheblock_size)
                # 将读入的数据转换为数组
                audio_data = np.fromstring(string_audio_data, dtype=np.short)
                # 样本值大于LEVEL的取样为成功取样，计算成功取样的样本的个数
                large_sample_count = np.sum(audio_data > self.level)
                print "Peak:",np.max(audio_data),"    Sum:",large_sample_count
                # 如果成功取样数大于SAMPLING_NUM，则此次取样成功
                if large_sample_count > self.sampling_num:
                    # 有成功取样的样本时，重新计数
                    silence_count = 0
                else:
                    # 取样失败（相当于模拟没有声音了）
                    silence_count += 1

                # 取样失败次数是否超过最大值
                if silence_count < self.max_silence_length:
                    # 将要保存的数据存放到save_buffer中
                    save_buffer.append(string_audio_data)
                else:
                    # 将save_buffer中的数据写入WAV文件，WAV文件的文件名是保存的时刻
                    if len(save_buffer) > 0:
                        rnfilename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + ".wav"
                        self.__Save_wave_file(rnfilename, save_buffer)
                        save_buffer = []
                        print rnfilename, "saved"
                    exit()
        except KeyboardInterrupt:
            print "manual exit"
        else:
            print "error"

        return rnfilename