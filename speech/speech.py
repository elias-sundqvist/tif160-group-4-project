import _thread
import speech_recognition as sp

rec = sp.Recognizer()
#my_micro = 

class Speech():
    def __init__(self):
        self.listeners = []

        def message_received(message):
            print("Message Received " + message)
            for listener in self.listeners:
                listener(message)

        def recognition_loop():
            with sp.Microphone(device_index=2, sample_rate=48000) as source: #change this to 1 when hdmi not connected! (2 when hdmi connected)
                while True:
                    try:
                        audio = rec.listen(source,6,6)
                        message_received(rec.recognize_google(audio))
                    except:
                        print("No message heard")
                        pass

        _thread.start_new_thread(recognition_loop, ())

    def add_listener(self, listener):
        self.listeners.append(listener)
