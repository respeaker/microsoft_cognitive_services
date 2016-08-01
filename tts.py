from bing_voice import *
import pyaudio
import sys

# get a key from https://www.microsoft.com/cognitive-services/en-us/speech-api
BING_KEY = ''
CHUNK_SIZE = 2048

if len(sys.argv) < 2:
    print('Usage: python %s text_to_convert' % sys.argv[0])
    sys.exit(-1)

bing = BingVoice(BING_KEY)
data = bing.synthesize(sys.argv[1])

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=16000,
                 output=True,
                 # output_device_index=1,
                 frames_per_buffer=CHUNK_SIZE)

stream.write(data)
stream.close()
