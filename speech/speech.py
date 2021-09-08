from speech.ws_speech import SpeechWebsocket
from speech.page_server import serve_page

serve_page()

class Speech(SpeechWebsocket):
    def __init__(self):
        super().__init__()