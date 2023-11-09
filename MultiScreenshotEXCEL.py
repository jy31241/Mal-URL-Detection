import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import os
import threading
import natsort

path = "C:/Users/Mini1/Desktop/개발/Targetfile/"
file_list = os.listdir(path)  # 디렉토리에 있는파일 리스트로 반환
file_list_with_path = [os.path.join(
    path, file) for file in file_list if file.endswith(".xlsx")]  # 파일 이름 앞에 경로를 붙여줌
final_list = natsort.natsorted(file_list_with_path)
for flist in (natsort.natsorted(file_list)):
    print(flist)


def Screenrun(target):

    result = pd.read_excel(target)
    url_list = result['Query'].tolist()
    urllen = len(url_list)

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    #service=ChromeService(ChromeDriverManager().install())
    service=ChromeService(executable_path=r'C:/Users/Mini1/.wdm/drivers/chromedriver/win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    timeout = 20
    count = 1

    for url in url_list:
        if not url.startswith('http'):
            url = 'http://' + url

        Purl = url[7:]  # http:// 부분 제거(파일 이름에 : / 같은거 못씀)
        # now = datetime.now()
        # Ktime = now.strftime('%Y%m%d-%H시%M분%S초')

        try:
            driver.set_page_load_timeout(timeout)
            driver.get(url)
            driver.save_screenshot(
                f"C:/Users/Mini1/Desktop/개발/WEB/static/images/{Purl}.png")  # 저장경로
            print(
                f'{url}: Good {threading.current_thread().name} -[{count}/{urllen}]')
            count += 1

        except:
            print(
                f'{url}: Error {threading.current_thread().name} -[{count}/{urllen}]')
            count += 1
    print(
        f"--------------------{threading.current_thread().name} Complete--------------------")


# 각 파일에 대해 쓰레드 생성하고 시작
threads = []
for file in final_list:
    t = threading.Thread(target=Screenrun, args=(file,))
    threads.append(t)
    t.start()

# 모든 쓰레드가 끝날 때까지 기다림
for t in threads:
    t.join()
