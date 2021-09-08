import webbrowser
import _thread
from http.server import HTTPServer, CGIHTTPRequestHandler
chromedir= "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"

def serve_page():
    server_object = HTTPServer(server_address=('', 1654), RequestHandlerClass=CGIHTTPRequestHandler)
    webbrowser.get(chromedir).open("http://localhost:1654/speech/test.html")
    _thread.start_new_thread(server_object.serve_forever, ())