'''
Bing Speech To Text (STT)

based on https://github.com/Uberi/speech_recognition

'''

import json
import uuid
import wave
import io
from monotonic import monotonic
from urllib import urlencode
from urllib2 import Request, urlopen, URLError, HTTPError


# get a key from https://www.microsoft.com/cognitive-services/en-us/speech-api
BING_KEY = ''


class RequestError(Exception):
    pass


class UnknownValueError(Exception):
    pass


class BingVoiceRecognizer():
    def __init__(self, key):
        self.key = key

    def recognize(self, audio_data, language="en-US", show_all=False):
        access_token, expire_time = getattr(self, "bing_cached_access_token", None), \
                                    getattr(self, "bing_cached_access_token_expiry", None)

        if expire_time is None or monotonic() > expire_time:  # first credential request, or the access token from the previous one expired
            # get an access token using OAuth
            credential_url = "https://oxford-speech.cloudapp.net/token/issueToken"
            credential_request = Request(credential_url, data=urlencode({
                "grant_type": "client_credentials",
                "client_id": "python",
                "client_secret": self.key,
                "scope": "https://speech.platform.bing.com"
            }).encode("utf-8"))
            start_time = monotonic()
            try:
                credential_response = urlopen(credential_request)
            except HTTPError as e:
                raise RequestError("recognition request failed: {0}".format(
                    getattr(e, "reason", "status {0}".format(e.code))))  # use getattr to be compatible with Python 2.6
            except URLError as e:
                raise RequestError("recognition connection failed: {0}".format(e.reason))
            credential_text = credential_response.read().decode("utf-8")
            credentials = json.loads(credential_text)
            access_token, expiry_seconds = credentials["access_token"], float(credentials["expires_in"])

            # save the token for the duration it is valid for
            self.bing_cached_access_token = access_token
            self.bing_cached_access_token_expiry = start_time + expiry_seconds

        wav_data = self.to_wav(audio_data)
        url = "https://speech.platform.bing.com/recognize/query?{0}".format(urlencode({
            "version": "3.0",
            "requestid": uuid.uuid4(),
            "appID": "D4D52672-91D7-4C74-8AD8-42B1D98141A5",
            "format": "json",
            "locale": language,
            "device.os": "wp7",
            "scenarios": "ulm",
            "instanceid": uuid.uuid4(),
            "result.profanitymarkup": "0",
        }))
        request = Request(url, data=wav_data, headers={
            "Authorization": "Bearer {0}".format(access_token),
            "Content-Type": "audio/wav; samplerate=16000; sourcerate={0}; trustsourcerate=true".format(16000),
        })
        try:
            response = urlopen(request)
        except HTTPError as e:
            raise RequestError("recognition request failed: {0}".format(
                getattr(e, "reason", "status {0}".format(e.code))))  # use getattr to be compatible with Python 2.6
        except URLError as e:
            raise RequestError("recognition connection failed: {0}".format(e.reason))
        response_text = response.read().decode("utf-8")
        result = json.loads(response_text)

        # return results
        if show_all: return result
        if "header" not in result or "lexical" not in result["header"]: raise UnknownValueError()
        return result["header"]["lexical"]

    @staticmethod
    def to_wav(raw_data):
        # generate the WAV file contents
        with io.BytesIO() as wav_file:
            wav_writer = wave.open(wav_file, "wb")
            try:  # note that we can't use context manager, since that was only added in Python 3.4
                wav_writer.setframerate(16000)
                wav_writer.setsampwidth(2)
                wav_writer.setnchannels(1)
                wav_writer.writeframes(raw_data)
                wav_data = wav_file.getvalue()
            finally:  # make sure resources are cleaned up
                wav_writer.close()
        return wav_data

        
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 2:
        print('Usage: %s 16k_mono.wav' % sys.argv[0])
        sys.exit(-1)
        
    wf = wave.open(sys.argv[1])
    if wf.getframerate() != 16000 or wf.getnchannels() != 1 or wf.getsampwidth() != 2:
        print('only support 16000 sample rate, 1 channel and 2 bytes sample width')
        sys.exit(-2)
    
    # read less than 10 seconds audio data
    n = wf.getnframes()
    if (n / 16000.0) > 10.0:
        n = 16000 * 10
        
    frames = wf.readframes(n)
        
    recognizer = BingVoiceRecognizer(BING_KEY)
    
    # recognize speech using Microsoft Bing Voice Recognition
    try:
        text = recognizer.recognize(frames, language='en-US')
        print('Bing:' + text.encode('utf-8'))
    except UnknownValueError:
        print("Microsoft Bing Voice Recognition could not understand audio")
    except RequestError as e:
        print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
        