Python scripts to use microsoft cognitive services
==================================================

1. Get a API key from [Microsoft](https://www.microsoft.com/cognitive-services/en-us/speech-api)
and add it to the Python scripts.
2. Install the required package `pip install monotonic`
3. Change the default language in the Python scripts from `language='zh-CN'` to your prefered language. For example `language='en-GB'`. A [complete list of supported languages is available from Microsoft](https://www.microsoft.com/cognitive-services/en-us/speech-api/documentation/overview).

### Speech To Text

+ bing_voice.py

  `python bing_voice.py sample.wav` recognizes audio from file (16000 sample rate, 1 channel)

+ bing_stt_with_vad.py

  Read audio from microphone, pre-process audio with voice activity detector (VAD) and then recognize

### Text To Speech
+ tts.py

  `python tts.py 'hello, Respeaker is being actively developed. Stay tuned'`
