import _thread
import logging
from websocket_server import WebsocketServer

class SpeechWebsocket():
    def __init__(self):
        server = WebsocketServer(1655, host='127.0.0.1', loglevel=logging.INFO)
        self.listeners = []

        def new_client(client, server):
            print("New Client!")
            pass

        def message_received(client, server, message):
            print("Message Received %s" % message)
            for listener in self.listeners:
                listener(message)

        server.set_fn_new_client(new_client)
        server.set_fn_message_received(message_received)
        _thread.start_new_thread(server.run_forever, ())

    def add_listener(self, listener):
        self.listeners.append(listener)