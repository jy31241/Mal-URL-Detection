import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

filepath = 'C:/Users/Mini1/Desktop/개발/Targetfile/Target.xlsx'
result = pd.read_excel(filepath)

url_list = result['URL'].tolist()
status_code_list = []
title_list = []
history_list = []
header_content_type_list = []
input_list = []
href_list = []
time_list = []
# reurl_list = []

options = webdriver.ChromeOptions() 
options.add_argument('headless')
options.add_argument('window-size=1920x1080')

urllen = len(url_list)
timeout = 10
stauts_count = 1
screen_count = 1

for url in url_list:
    if not url.startswith('http'):
        url = 'http://' + url
        try:
            response = requests.get(url, timeout=timeout, allow_redirects=True)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            status_code_list.append(response.status_code)
            title_list.append(soup.title.string)
            history_list.append(response.history)
            header_content_type_list.append(response.headers['Content-Type'])
            input_list.append(soup.find_all('input'))
            href_list.append(soup.find_all('a'))
            # reurl_list.append(response.url)

            print(f'{url}: Good, [{stauts_count}/{urllen}]')
            stauts_count += 1

        except:
            status_code_list.append('Error')
            title_list.append('Error')
            history_list.append('Error')
            header_content_type_list.append('Error')
            input_list.append('Error')
            href_list.append('Error')
            # reurl_list.append('Error')

            print(f'{url}: Error, [{stauts_count}/{urllen}]')
            stauts_count += 1

    time_list.append(datetime.now())

# df['Re URL'] = pd.Series(reurl_list)
result['Status Code'] = pd.Series(status_code_list)
result['HTML Title'] = pd.Series(title_list)
result['Redirection history'] = pd.Series(history_list)
result['Content_type'] = pd.Series(header_content_type_list)
result['Input'] = pd.Series(input_list)
result['Href'] = pd.Series(href_list)
result['Time'] = pd.Series(time_list)

result.to_excel(filepath, index=False)
print('--------------------Excel Complete--------------------')

for url in url_list:
    if not url.startswith('http'):
        url = 'http://' + url

    driver = webdriver.Chrome(service=Service(
        executable_path=ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(timeout)

    now = datetime.now()
    Ktime = now.strftime('%Y%m%d-%H시%M분%S초')
    Purl = url[7:]  # http:// 부분 제거(파일 이름에 : / 같은거 못씀)

    try:
        driver.get(url)
        driver.save_screenshot(
            f"C:/Users/Mini1/Desktop/개발/Screenshot/{Purl}_{Ktime}.png")
        print(f'{url}: Good, [{screen_count}/{urllen}]')
        screen_count += 1

    except:
        print(f'{url}: Error, [{screen_count}/{urllen}]')
        screen_count += 1
print('--------------------ScreenShot Complete--------------------')