import _thread
import speech_recognition as sp

rec = sp.Recognizer()
my_micro = sp.Microphone(device_index=1)

class Speech():
    def __init__(self):
        self.listeners = []

        def message_received(message):
            print("Message Received %s" % message)
            for listener in self.listeners:
                listener(message)

        def recognition_loop():
            with my_micro as source:
                while True:
                    try:
                        audio = rec.listen(source, 2, 2)
                        message_received(rec.recognize_google(audio))
                    except:
                        print("No message heard")
                        pass

        _thread.start_new_thread(recognition_loop, ())

    def add_listener(self, listener):
        self.listeners.append(listener)
