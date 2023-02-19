import numpy as np
# Speech to Text
api_key = '9283c8042f454c4d8638fca0484512ab'
endpoint = 'https://centralindia.api.cognitive.microsoft.com/sts/v1.0/issuetoken'
import azure.cognitiveservices.speech as speechsdk

# To ignore Warnings
import warnings

warnings.simplefilter(action='ignore')

import pickle

data = pickle.load(open('data.pkl', 'rb'))

X = data['data']
y = data['class']

cv = pickle.load(open('cv.pkl','rb'))
X_ = cv.fit_transform(X)

X_ = X_.toarray()

model = pickle.load(open('model.pkl', 'rb'))


def detect_hate_speech(sample):
    vect = cv.transform(sample).toarray()
    pred_prob = np.max(model.predict_proba(vect))
    pred = model.predict(vect)

    return pred, pred_prob


def detect(sample):
    hatespeech = detect_hate_speech(sample)
    mp = "Try again"
    if hatespeech[0] == 0:
        mp = "Hate Speech Detected"
    elif hatespeech[0] == 1:
        mp = "Offensive Language Detected"
    elif hatespeech[0] == 2:
        mp = "NO Hate Speech Detected"

    return mp, hatespeech[1], hatespeech[0]

def voice_file(file):
    speech_config = speechsdk.SpeechConfig(subscription=api_key, endpoint=endpoint)
    speech_config.speech_recognition_language = "en-US"

    speech_config.set_profanity(speechsdk.ProfanityOption.Raw)

    audio_config = speechsdk.audio.AudioConfig(filename=file)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return speech_recognition_result.text
    elif speech_recognition_result.text =="":
        return "No hate speech detected"