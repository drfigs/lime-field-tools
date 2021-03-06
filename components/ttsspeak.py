# Find some kind of TTS functionality and assign it to ttsSpeak
# On OSX, we look for:
#     say: A TTS program included with OSX
#          http://developer.apple.com/library/mac/#documentation/Darwin/Reference/ManPages/man1/say.1.html
#     espeak: A free TTS program for Linux, Windows and OSX
#             http://espeak.sourceforge.net/
# On Linux, we look for:
#     espeak: A free TTS program for Linux, Windows and OSX
#             http://espeak.sourceforge.net/
#     flite, A free TTS program for Linux
#            http://www.speech.cs.cmu.edu/flite/
# On Windows, we look for:
#     espeak: A free TTS program for Linux, Windows and OSX
#             http://espeak.sourceforge.net/
# On Android we use the TTS feature included with Android.
# If no TTS is found, we use notts, which just echoes the message to the console
#
# Usage:
# from components.ttsspeak import TtsSpeak
# TtsSpeak('what you want said').speak()


from kivy.utils import platform

platform = platform()


class TtsSpeakBase():
    ''' Default TTS Speech class. 
        Override the speak method to implement new versions.
    '''
    def __init__(self, message):
        self.message = message
        
    def speak(self):
        ''' Echoes the message to the console '''
        print('TTS: {}'.format(self.message))

    def stop(self):
        pass

class TtsSpeakAndroid(TtsSpeakBase):

    def __init__(self, message):
        self.message = message
#        super(TtsSpeakAndroid, self).__init__(message)
        from jnius import autoclass
        Locale = autoclass('java.util.Locale')
        PythonActivity = autoclass('org.renpy.android.PythonActivity')
        self.TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
        self.tts = self.TextToSpeech(PythonActivity.mActivity, None)
#        self.tts.setLanguage(Locale.US)

    def speak(self):
        ''' Speaks using the built-in Android TTS feature '''
        from time import sleep
        self.tts.setSpeechRate(1.5)
        retries = 0
        if self.tts.isSpeaking():
            return
        else:
            self.tts.speak(self.message.encode('utf-8'), self.TextToSpeech.QUEUE_FLUSH, None)

    def stop(self):
        self.tts.stop()

class TtsSpeakEspeak(TtsSpeakBase):
    def speak(self):
        ''' Speaks the message using espeak '''
        import subprocess
        subprocess.call(["espeak", self.message])


class TtsSpeakFlite(TtsSpeakBase):
    def speak(self):
        ''' Speaks the message using flite '''
        import subprocess
        subprocess.call(["flite", "-t", self.message, "play"])
    

class TtsSpeakOsx(TtsSpeakBase):
    def speak(self):
        ''' Speaks the message using built-in OSX TTS '''
        import subprocess
        subprocess.call(["say", self.message])


# Default to notts
TtsSpeak = TtsSpeakBase

# Platform-specific searches
if platform == "android":
    TtsSpeak = TtsSpeakAndroid
    
if platform == "macosx":
    from components import whereis_exe
    if whereis_exe('say'):
        TtsSpeak = TtsSpeakOsx
    elif whereis_exe('espeak'):
        TtsSpeak = TtsSpeakEspeak
    
elif platform == "linux":
    from components import whereis_exe
    if whereis_exe('espeak'):
        TtsSpeak = TtsSpeakEspeak
    elif whereis_exe('flite'):
        TtsSpeak = TtsSpeakFlite
        
elif platform == "win":
    from components import whereis_exe
    if whereis_exe('espeak'):
        TssSpeak = TtsSpeakEspeak
