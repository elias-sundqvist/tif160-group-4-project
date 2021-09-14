import _thread
import os
from http.server import HTTPServer, CGIHTTPRequestHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROMEDRIVER_PATH = "/usr/lib/chromium-browser/chromedriver";
options = Options()
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1
  })
options.add_argument("--use-fake-ui-for-media-stream")
options.add_argument("--disable-user-media-security")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

def serve_page():
    server_object = HTTPServer(server_address=('', 1654), RequestHandlerClass=CGIHTTPRequestHandler)
    _thread.start_new_thread(server_object.serve_forever, ())
    print("Trying to initialize headless chrome...")
    driver.get("http://localhost:1654/speech/test.html")
    print("Headless Chrome Initialized")