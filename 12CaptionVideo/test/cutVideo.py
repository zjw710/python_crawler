#coding=utf-8
'''
裁切音频文件
'''

from pydub import AudioSegment

wav = AudioSegment.from_mp3('csbTmp.mp3')
wav[0:10000].export('./cut_file/csbTmp0_10000.wav', format="wav")
# wav[797:2067].export('./cut_file/test797_2067.wav', format="wav")
# wav[2343:3698].export('./cut_file/test2343_3698.wav', format="wav")
# wav[4219:5112].export('./cut_file/test4219_5112.wav', format="wav")
# wav[5439:6323].export('./cut_file/test5439_6323.wav', format="wav")
# wav[6840:].export('./cut_file/test6840_0.wav', format="wav")