# -*- coding: utf-8 -*-
import sys
sys.path.append("./voc")

from rnaudio import *

# 录音测试
rna = Rnaudio()
filename = rna.Record()
rna.Play_WAV(filename)
rna.Delete(filename)
