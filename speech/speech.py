import _thread

from speech.ws_speech import SpeechWebsocket
from speech.page_server import serve_page

class Speech(SpeechWebsocket):
    def __init__(self):
        _thread.start_new_thread(serve_page, ())
        super().__init__()