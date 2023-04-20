import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

filepath = 'C:/Users/Mini1/Desktop/개발/Targetfile/230402_query_iptime(0401~0420).xlsx'
result = pd.read_excel(filepath)
url_list = result['URL'].tolist()

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')

urllen = len(url_list)
timeout = 10
count = 1

for url in url_list:
    if not url.startswith('http'):
        url = 'http://' + url

    now = datetime.now()
    Ktime = now.strftime('%Y%m%d-%H시%M분%S초')
    Purl = url[7:]  # http:// 부분 제거(파일 이름에 : / 같은거 못씀)

    try:
        driver = webdriver.Chrome(service=Service(
        executable_path=ChromeDriverManager().install()), options=options)
        driver.set_page_load_timeout(timeout)
        driver.get(url)
        driver.save_screenshot(
            f"C:/Users/Mini1/Desktop/개발/Screenshot/{Purl}_{Ktime}.png")
        print(f'{url}: Good, [{count}/{urllen}]')
        count += 1

    except:
        print(f'{url}: Error, [{count}/{urllen}]')
        count+=1
print('--------------------Screenshot Complete--------------------')