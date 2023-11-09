import requests
import pandas as pd
from bs4 import BeautifulSoup
# from datetime import datetime
import os
import threading
import natsort

path = "C:/Users/Mini1/Desktop/개발/Targetfile/"
file_list = os.listdir(path)  # 디렉토리에 있는파일 리스트로 반환
file_list_with_path = [os.path.join(
    path, file) for file in file_list if file.endswith(".xlsx")]  # 파일 이름 앞에 경로를 붙여줌
final_list = natsort.natsorted(file_list_with_path) # 최종 분석대상 리스트
for flist in (natsort.natsorted(file_list)): # 그냥 cmd 출력용
    print(flist)

def Statusrun(target):
    result = pd.read_excel(target)
    url_list = result['Query'].tolist()
    status_code_list = []
    title_list = []
    history_list = []
    # input_list = []
    href_list = []
    form_list = []
    head_list = []
    # html_text_list = []
    reurl_list = []
    headers_list = []
    urllen = len(url_list)
    timeout = 12
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
                headers_list.append(response.headers) #Content-Disposition값이 attachment 유무(파일 다운로드) 확인
                # if 'Content-Disposition' in response.headers:
                #     content_disposition = response.headers['Content-Disposition']
                #     if 'attachment' in content_disposition:
                #         headers_list.append('파일 다운로드 실행')
            except:
                headers_list.append('Error')

            try:
                history_list.append(response.history)
            except:
                history_list.append('Error')

            try:
                title_list.append(soup.title.string)
            except:
                title_list.append('Error')

            # try:
            #     input_list.append(soup.find_all('input'))
            # except:
            #     input_list.append('Error')

            try:
                form_list.append(soup.find_all('form'))
            except:
                form_list.append('Error')
           
            try:
                head_list.append(soup.find_all('head'))
            except:
                head_list.append('Error')

            try:
                href_list.append(soup.find_all('a'))
            except:
                href_list.append('Error')

            # try:
            #     html_text_list.append(response.text())
            # except:
            #     html_text_list.append('Error')

        result['Status Code'] = pd.Series(status_code_list)
        result['End URL'] = pd.Series(reurl_list)
        result['Headers'] = pd.Series(headers_list)
        result['Redirection history'] = pd.Series(history_list)
        result['Title'] = pd.Series(title_list)
#       result['Input'] = pd.Series(input_list)
        result['Form'] = pd.Series(form_list)
        result['Head'] = pd.Series(head_list)
        result['a Tag'] = pd.Series(href_list)
        # result['HTML ALL'] = pd.Series(html_text_list)

        try:
            result.to_excel(target, index=False)
            print(f'{url}: Good {threading.current_thread().name} -[{count}/{urllen}]')
        except:
            print(f'{url}: Error {threading.current_thread().name} -[{count}/{urllen}]')
        count += 1
    print(f"--------------------{threading.current_thread().name} Complete--------------------")

# 각 파일에 대해 쓰레드 생성하고 시작
threads = []

for file in final_list:
    t = threading.Thread(target=Statusrun, args=(file,))
    threads.append(t)
    t.start()

# 모든 쓰레드가 끝날 때까지 기다림
for t in threads:
    t.join()