from scipy.io import wavfile as wav
from scipy.fftpack import fft
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt

import time
# audio config params
FORMAT = pyaudio.paInt16  # format of sampling 16 bit int
CHANNELS = 1  # number of channels it means number of sample in every sampling
RATE = 44100  # number of  sample in 1 second sampling
CHUNK = 1024  # length of every chunk
RECORD_SECONDS = 1  # time of recording in seconds
WAVE_OUTPUT_FILENAME = "file.wav"  # file name
FREQBANDS = 128

refrence_records = []
audio = pyaudio.PyAudio()
for record in ["1","2","3","4","5","6","7","8","9","10"]:
    # print("Start recording"+record)
    # stream = audio.open(
    #     format=FORMAT,
    #     channels=CHANNELS,
    #     rate=RATE,
    #     input=True,
    #     frames_per_buffer=CHUNK
    # )

    # frames = []

    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #     data = stream.read(CHUNK)
    #     frames.append(data)
    # print("finished recording")

    # # stop Recording
    # stream.stop_stream()
    # stream.close()

    # # storing voice
    # waveFile = wave.open(record+".wav", 'wb')
    # waveFile.setnchannels(CHANNELS)
    # waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    # waveFile.setframerate(RATE)
    # waveFile.writeframes(b''.join(frames))
    # waveFile.close()

    rate, data = wav.read(record+".wav")

    pow_audio_signal = data / np.power(2, 15)
    pow_audio_signal = pow_audio_signal [:100]

    sig_length = len(pow_audio_signal)
    half_length = np.ceil((sig_length + 1) / 2.0).astype(np.int)

    vc = np.fft.fft(data)
    abs_vc = np.absolute(vc)
    abs_vc = abs_vc[0:int(len(abs_vc)/2)]/len(pow_audio_signal)

    freqspectrm = [0] * FREQBANDS 

    total_energy = np.sum(abs_vc)



    for freq in range(len(abs_vc)) :
        if freq < 8000:
            freqband = int(freq/(8000/FREQBANDS))
            freqspectrm[freqband] += abs_vc[freq]

    for i in range(FREQBANDS):
        freqspectrm[i] /= total_energy
    
    refrence_records.append(freqspectrm)

    # plotting
#     plt.title("Line graph")
#     plt.xlabel("Freq band")
#     plt.ylabel("Energy")
#     plt.plot(np.arange(0,FREQBANDS), freqspectrm)

# plt.show()
# print(refrence_records)

while True:
    # start Recording
    print("Start recording")
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()

    # storing voice
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    rate, data = wav.read(WAVE_OUTPUT_FILENAME)
    # rate, data = wav.read("4.wav")

    pow_audio_signal = data / np.power(2, 15)
    pow_audio_signal = pow_audio_signal [:100]

    sig_length = len(pow_audio_signal)
    half_length = np.ceil((sig_length + 1) / 2.0).astype(np.int)

    vc = np.fft.fft(data)
    abs_vc = np.absolute(vc)

    # time_axis = 1000 * np.arange(0, len(pow_audio_signal), 1) / float(rate)
    # plt.plot(np.arange(0,len(abs_vc)), abs_vc)
    # plt.show()

    abs_vc = abs_vc[0:int(len(abs_vc)/2)]/len(pow_audio_signal)

    freqspectrm = [0] * FREQBANDS 

    total_energy = np.sum(abs_vc)



    for freq in range(len(abs_vc)) :
        if freq < 8000:
            freqband = int(freq/(8000/FREQBANDS))
            freqspectrm[freqband] += abs_vc[freq]
            
    for i in range(FREQBANDS):
        freqspectrm[i] /= total_energy

    probabilty_vector = [0]*len(refrence_records)
    for i in range(len(refrence_records)):
        # probabilty_vector[i] = np.linalg.norm(freqspectrm - refrence_records[i])
        for j in range(len(freqspectrm)):
            probabilty_vector[i] += (freqspectrm[j] - refrence_records[i][j])**2

    probabilty_vector /= np.max(probabilty_vector)
    probabilty_vector = 1 - probabilty_vector


    max = probabilty_vector[0]
    index = 0
    for i in range(1,len(probabilty_vector)):
        if probabilty_vector[i] > max:
            max = probabilty_vector[i]
            index = i
    if max > 0.7:
        print(index+1)

    plt.title("Line graph")
    plt.xlabel("number")
    plt.ylabel("prob")
    plt.plot(np.arange(1,1+len(refrence_records)), probabilty_vector)

    plt.xticks(np.arange(1,1+len(refrence_records)), [1,2,3,4,5,6,7,8,9,10])

    plt.show()
    time.sleep(2)
    


audio.close()
