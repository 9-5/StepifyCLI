import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def getCSRFToken():
    opt = Options()
    opt.add_argument("--headless")
    opt.add_argument("--log-level=3")
    opt.add_argument("--disable-gpu")
    opt.add_argument("--no-sandbox")

    DRIVER = webdriver.Chrome(options=opt)
    DRIVER.get("https://stepify.tech/")
    session_cookie = DRIVER.get_cookie("session")["value"]
    print(session_cookie)
    csrf_token = DRIVER.execute_script("""
        var element = document.getElementById('csrf_token');
        return element ? element.value : null;
    """)
    DRIVER.quit()
    return csrf_token, session_cookie

def sendRequest(csrf_token, session_cookie, yt_url):
    url = "https://stepify.tech/"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": f"session={session_cookie}",
        "Origin": "https://stepify.tech",
        "Referer": "https://stepify.tech/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
        # Adjusted the sec-ch-ua header for Python compatibility
        "sec-ch-ua": '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        "sec-ch-ua-mobile": "?0",
        # Adjusted the sec-ch-ua-platform header for Python compatibility
        "sec-ch-ua-platform": '"Windows"'
    }

    data = f"csrf_token={csrf_token}&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D{yt_url}"

    requests.post(url, headers=headers, data=data)
    time.sleep(10)
    print("https://stepify.tech/video/" + yt_url)

csrf_token, session_cookie = getCSRFToken()
yt_url = input("Enter YouTube URL: ").split("=")[1]
sendRequest(csrf_token, session_cookie, yt_url)
