# -*- coding: utf-8 -*-
import os
from pyaudio import PyAudio, paInt16
import wave
from datetime import datetime
import numpy as np 

CHANNELS = 1    # 声道数
SAMPWIDTH = 2   # 量化位数

class Rnaudio(object):
    # 初始化：类似于构造函数
    def __init__(self):
        # 初始化录音变量，各个字段的意思详见各自的属性定义块
        self.__cacheblock_size = 1024
        self.__sampling_rate = 8000
        self.__level = 1000
        self.__sampling_num = 20
        self.__max_save_length = 16
        self.__max_silence_length = 8
        self.__filename = ""
    
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
    
    # max_save_length：最大记录长度
    @property
    def max_save_length(self):
        return self.__max_save_length
    @max_save_length.setter
    def max_save_length(self, rlen):
        self.__max_save_length = rlen

    # max_silence_length：最大静音块长度
    @property
    def max_silence_length(self):
        return self.__max_silence_length
    @max_silence_length.setter
    def max_silence_length(self, slen):
        self.max_silence_length = slen

    # filename：文件名
    @property
    def filename(self):
        return self.__filename
    @filename.setter
    def filename(self, fn):
        self.__filename = fn

    # 私有函数：将data中的数据保存到名为FILENAME的WAV文件中
    def __Save_wave_file(self, filename, data):
        global CHANNELS
        global SAMPWIDTH
        wf = wave.open(filename, 'wb')
        # 配置声道数、量化位数和取样频率
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(SAMPWIDTH)
        wf.setframerate(self.sampling_rate)
        wf.writeframes("".join(data))
        wf.close()

    # 公有函数：开始录音-->存储录音文件-->返回录音文件名
    def Record(self):
        global CHANNELS

        # 开启声音输入
        pa = PyAudio()
        stream = pa.open(format=paInt16, channels=CHANNELS, rate=self.sampling_rate, input=True, 
                        frames_per_buffer=self.cacheblock_size)

        save_count = 0          # 已经保存的样本块
        silence_count = 0       # 持续无声音的样本块
        save_buffer = []        # 音频缓冲

        try:
            print "start recording"
            while True:
                # 录音、取样
                string_audio_data = stream.read(self.cacheblock_size)
                # 将读入的数据转换为数组
                audio_data = np.fromstring(string_audio_data, dtype=np.short)
                # 样本值大于LEVEL的取样为成功取样，计算成功取样的样本的个数
                large_sample_count = np.sum(audio_data > self.level)
                print "Peak:",np.max(audio_data),"    Sum:",large_sample_count
                # 如果成功取样数大于SAMPLING_NUM，则当前数据块取样都成功
                if large_sample_count > self.sampling_num:
                    # 有成功取样的数据块时，样本计数+1
                    save_count += 1
                else:
                    # 有成功录取的块后，若取样失败，此时可能处于静音状态，静音计数+1
                    if(save_count > 0):
                        silence_count += 1

                # 取样失败次数是否超过最大值
                if (save_count <= self.max_save_length) and (silence_count <= self.max_silence_length):
                    # 将要保存的数据存放到save_buffer中
                    save_buffer.append(string_audio_data)
                else:
                    # 将save_buffer中的数据写入WAV文件，WAV文件的文件名是保存的时刻
                    if len(save_buffer) > 0:
                        self.filename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + ".wav"
                        self.__Save_wave_file(self.filename, save_buffer)
                        save_buffer = []
                        print self.filename, "saved"
                    break
        except KeyboardInterrupt:
            print "manual exit"
        finally:
            # stop stream
            stream.stop_stream()  
            stream.close()
            # close PyAudio  
            pa.terminate() 
            print "exit recording"

        return self.filename

    def Play(self, filename):
        chunk = 1024
        f = wave.open(filename,"rb")
        pa = PyAudio()

        # open stream
        stream = pa.open(format = pa.get_format_from_width(f.getsampwidth()),  
                        channels = f.getnchannels(),  
                        rate = f.getframerate(),  
                        output = True)

        # read data
        data = f.readframes(chunk)
        # play stream
        while data != '':
            stream.write(data)
            data = f.readframes(chunk)

        # stop stream
        stream.stop_stream() 
        stream.close()
        # close PyAudio  
        pa.terminate() 

    def Delete(self, filename):
        os.remove(filename)
        print filename,"removed"

    