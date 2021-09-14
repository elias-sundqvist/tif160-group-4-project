import _thread
import os
from http.server import HTTPServer, CGIHTTPRequestHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chromedir= "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"

CHROMEDRIVER_PATH = os.getcwd()+"/chromedriver.exe";
options = Options()
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1
  })
#options.headless = True
options.add_argument("--use-fake-ui-for-media-stream")
options.add_argument("--disable-user-media-security")
driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
driver.minimize_window()

def serve_page():
    server_object = HTTPServer(server_address=('', 1654), RequestHandlerClass=CGIHTTPRequestHandler)
    _thread.start_new_thread(server_object.serve_forever, ())
    print("Trying to initialize headless chrome...")
    driver.get("http://localhost:1654/speech/test.html")
    print("Headless Chrome Initialized")