import requests, time, tempfile, os, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    """
    Custom HTML parser that extracts the content of an article tag.
    """
    def __init__(self):
        super().__init__()
        self.article_content = ""

    def handle_data(self, data):
        """
        Appends the data to the article content.
        """
        self.article_content += data

    def handle_starttag(self, tag, attrs):
        """
        Handles the start tag of an article tag. Resets the article content.
        Handles the end tag of an article tag. Trims the article content.
        """
        if tag == "article":
            self.article_content = ""
        elif tag == "/article":
            self.article_content = self.article_content.strip()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def getCSRFToken():
    """
    Retrieves the CSRF token and session cookie by automating Chrome.
    Returns the CSRF token and session cookie.
    """
    opt = webdriver.ChromeOptions()
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    opt.add_argument("--headless")
    opt.add_argument("--log-level=3")
    opt.add_argument("--disable-gpu")
    opt.add_argument("--no-sandbox")
    opt.add_argument("start-maximized")

    DRIVER = webdriver.Chrome(options=opt)
    clear()
    DRIVER.get("https://stepify.tech/")
    clear()
    session_cookie = DRIVER.get_cookie("session")["value"]
    csrf_token = DRIVER.execute_script("""
        var element = document.getElementById('csrf_token');
        return element ? element.value : null;
    """)
    DRIVER.quit()
    return csrf_token, session_cookie

def sendRequest(csrf_token, session_cookie, yt_url):
    """
    Sends a request to the Stepify API and processes the response.
    """
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
        "sec-ch-ua": '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }

    data = f"csrf_token={csrf_token}&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D{yt_url}"

    response = requests.post(url, headers=headers, data=data, timeout=60)
    while True:
        time.sleep(3)
        if response.status_code == 500:
            print(response.text)
        elif response.status_code == 200:
            parser = MyHTMLParser()
            parser.feed(response.text)
            article_content = parser.article_content
            temp_file_path = save_to_temp_file(cleanup_article_content(article_content))
            display_with_more(temp_file_path)
            break
        elif response.status_code == 320:
            print(response.text)
        else:
            print(f"Request failed with status code {response.status_code}")

def cleanup_article_content(input_text):
    """
    Extracts the content between "Introduction" and "Conclusion" from the input text.
    Returns the extracted content.
    """
    try:
        start = input_text.index("Introduction")
        end = input_text.index("Conclusion", start) + len("Conclusion")
        return input_text[start:end]
    except ValueError:
        print("Either 'Introduction' or 'Conclusion' not found.")
        return None

def save_to_temp_file(content):
    """
    Saves the content to a temporary file and returns the file path.
    """
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.html') as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name
    return temp_file_path

def display_with_more(temp_file_path):
    """
    Displays the content of the temporary file with a pause between each 10 lines.
    """
    try:
        with open(temp_file_path, 'r') as file:
            lines = file.readlines()
            num_lines = len(lines)
            for i in range(0, num_lines, 10):
                print('\n'.join(lines[i:min(i + 10, num_lines)]))
                input("Press Enter to display the next 5 lines...")
    except Exception as e:
        print(f"Error displaying file: {e}")
    finally:
        os.remove(temp_file_path)

csrf_token, session_cookie = getCSRFToken()
if len(sys.argv) > 1:
    yt_url = sys.argv[1].split("=")[1]
else:
    yt_url = input("Enter YouTube URL: ").split("=")[1]
sendRequest(csrf_token, session_cookie, yt_url)
