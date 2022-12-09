import speech_commands as sp
from ubinascii import a2b_base64, b2a_base64

data = a2b_base64('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')
sp.init(data)
labels = ["0","1","[OTHER]"]
feature = bytearray(732)

def predict(audio):
    result = sp.predict(audio, 0, 0)
    return (labels[result // 1000], result % 1000)

def snapshot():
    global feature
    sp.export_mfcc(feature)

def save(label):
    with open('samples.txt', 'ab') as f:
        f.write(b'{"label": "')
        f.write(label.encode())
        f.write(b'", "mfcc": "')
        f.write(b2a_base64(feature)[:-1])
        f.write(b'"},\n')
