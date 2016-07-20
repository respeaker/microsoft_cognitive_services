Python scripts to use microsoft cognitive services
==================================================

First, get a API key from [Microsoft](https://www.microsoft.com/cognitive-services/en-us/speech-api)
and add it to those scripts.

### Speech To Text

+ bing_recognizer.py

  `python bing_recognizer.py sample.wav` recognizes audio from file (16000 sample rate, 1 channel)

+ bing_stt_with_vad.py

  Read audio from micphone, pre-process audio with voice activity detector (VAD) and then recognize 
