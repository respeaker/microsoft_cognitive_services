Python scripts to use microsoft cognitive services
==================================================

First, get a API key from [Microsoft](https://www.microsoft.com/cognitive-services/en-us/speech-api)
and add it to those scripts.

### Speech To Text

+ bing_voice.py

  `python bing_voice.py sample.wav` recognizes audio from file (16000 sample rate, 1 channel)

+ bing_stt_with_vad.py

  Read audio from microphone, pre-process audio with voice activity detector (VAD) and then recognize

### Text To Speech
+ tts.py

  `python tts.py 'hello, Respeaker is being actively developed. Stay tuned'`