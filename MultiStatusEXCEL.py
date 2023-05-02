import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import os
import threading

path = "C:/Users/Mini1/Desktop/개발/Targetfile/"
file_list = os.listdir(path)  # 디렉토리에 있는파일 리스트로 반환
file_list_with_path = [os.path.join(
    path, file) for file in file_list if file.endswith(".xlsx")]  # 파일 이름 앞에 경로를 붙여줌
print(f"대상파일 리스트 경로:{file_list_with_path}")

def Statusrun(target):
    result = pd.read_excel(target)
    url_list = result['URL'].tolist()
    status_code_list = []
    title_list = []
    history_list = []
    # header_content_type_list = []
    input_list = []
    href_list = []
    form_list = []
    time_list = []
    reurl_list = []
    urllen = len(url_list)
    timeout = 10
    count = 1

    for url in url_list:
        if not url.startswith('http'):
            url = 'http://' + url

            try:
                response = requests.get(
                    url, timeout=timeout, allow_redirects=True)
                soup = BeautifulSoup(response.content, 'html.parser')
                status_code_list.append(response.status_code)
            except:
                status_code_list.append('Error')

            try:
                reurl_list.append(response.url)
            except:
                reurl_list.append('Error')

            try:
                history_list.append(response.history)
            except:
                history_list.append('Error')

            try:
                title_list.append(soup.title.string)
            except:
                title_list.append('Error')

            try:
                input_list.append(soup.find_all('input'))
            except:
                input_list.append('Error')

            try:
                form_list.append(soup.find_all('form'))
            except:
                form_list.append('Error')

            try:
                href_list.append(soup.find_all('a'))
            except:
                href_list.append('Error')

#           try:
#               response = requests.get(url, timeout=timeout, allow_redirects=True)
#               header_content_type_list.append(response.headers['Content-Type'])
#           except:
#               header_content_type_list.append('Error')

            time_list.append(datetime.now())
            result['Status Code'] = pd.Series(status_code_list)
            result['HTML Title'] = pd.Series(title_list)
            result['Redirection history'] = pd.Series(history_list)
            result['Input'] = pd.Series(input_list)
            result['Form'] = pd.Series(form_list)
            result['Href'] = pd.Series(href_list)
            result['End URL'] = pd.Series(reurl_list)
            result['Time'] = pd.Series(time_list)
            # result['Content_type'] = pd.Series(header_content_type_list)

        try:
            result.to_excel(target, index=False)
            print(f'{url}: Good [{count}/{urllen}]')
        except:
            print(f'{url}: Error [{count}/{urllen}]')
        count += 1
    print(f"--------------------Excel Complete--------------------")


# 각 파일에 대해 쓰레드 생성하고 시작
threads = []
for file in file_list_with_path:
    t = threading.Thread(target=Statusrun, args=(file,))
    threads.append(t)
    t.start()

# 모든 쓰레드가 끝날 때까지 기다림
for t in threads:
    t.join()
