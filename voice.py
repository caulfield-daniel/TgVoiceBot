import pyttsx3

voice = pyttsx3.init()

def get_voices():
    voices = voice.getProperty('voices')
    return voices

def get_current_voice():
    curr_voice = voice.getProperty('voice')
    return curr_voice