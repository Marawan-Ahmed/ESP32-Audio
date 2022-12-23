from scipy.io import wavfile as wav
from scipy.fftpack import fft
import pyaudio
import wave
import numpy as np
from numpy.linalg import norm
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
sample_per_record = 10
audio = pyaudio.PyAudio()

def get_fft(Sample):
    rate, data = wav.read(Sample)

    pow_audio_signal = data / np.power(2, 15)
    pow_audio_signal = pow_audio_signal [:100]

    sig_length = len(pow_audio_signal)
    # half_length = np.ceil((sig_length + 1) / 2.0).astype(np.int)

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
    
    return (freqspectrm)

def record_sample(output_file):
    # start Recording
    print("Start recording " + output_file )
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
    waveFile = wave.open(output_file, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def get_simlarity(vect1 , vect2):
    similarity_factor = np.sum(np.square(np.subtract(vect1,vect2)))
    # similarity_factor = np.dot(vect1,vect2)/(norm(vect1)*norm(vect2))
    return similarity_factor

for record in ["1","2","3","4","5","6","7","8","9","10"]:   
    temp_arr = []
    for sample in range (sample_per_record):
    # record_sample(record+".wav")

        temp_vect = get_fft(record+"_"+str(sample)+".wav")
        temp_arr.append(temp_vect)
    # plt.plot(np.arange(0,len(temp)), temp)
    refrence_records.append(temp_arr)

# plt.show()


while True:
    record_sample(WAVE_OUTPUT_FILENAME)
    sample_vector = get_fft(WAVE_OUTPUT_FILENAME)

    probabilty_vector = [0]*len(refrence_records)
    for record in range(len(refrence_records)):
        for sample in range(sample_per_record):
            probabilty_vector[record] += get_simlarity(sample_vector, refrence_records[record][sample])

    # probabilty_vector /= (np.max(probabilty_vector) * sample_per_record)
    # probabilty_vector = 1 - probabilty_vector


    max = probabilty_vector[0]
    index = 0
    for i in range(1,len(probabilty_vector)):
        if probabilty_vector[i] > max:
            max = probabilty_vector[i]
            index = i
    if max > 5:
        print(index+1)

    plt.title("Line graph")
    plt.xlabel("number")
    plt.ylabel("prob")
    plt.plot(np.arange(1,1+len(refrence_records)), probabilty_vector)

    plt.xticks(np.arange(1,1+len(refrence_records)), [1,2,3,4,5,6,7,8,9,10])

    plt.show()
    time.sleep(2)
    


audio.close()
