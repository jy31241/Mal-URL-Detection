import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
import threading
import natsort

path = "C:/Users/Mini1/Desktop/개발/Targetfile/"
file_list = os.listdir(path)  # 디렉토리에 있는파일 리스트로 반환
file_list_with_path = [os.path.join(
    path, file) for file in file_list if file.endswith(".xlsx")]  # 파일 이름 앞에 경로를 붙여줌
final_list = natsort.natsorted(file_list_with_path)  # 최종 분석대상 리스트
for flist in (natsort.natsorted(file_list)):  # 그냥 cmd 출력용
    print(flist)


def Statusrun(target):
    result = pd.read_excel(target)
    url_list = result['Query'].tolist()
    status_code_list = []
    title_list = []
    naver_logo_list = []
    naver_footer_list = []
    kakao_logo_list = []
    kakao_footer_list = []
    reurl_list = []
    urllen = len(url_list)
    timeout = 15
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
                title_list.append(soup.title.string)
            except:
                title_list.append('Error')

            try:
                naver_logo = soup.find_all('a', class_='logo')
                if naver_logo:
                    for tag in naver_logo:
                        if tag.get('href').startswith('https://www.naver.com') and tag.find('h1', class_='blind') and 'NAVER' in tag.text:
                            naver_logo_list.append('Find Naver Logo in HTML')
                else:
                    naver_logo_list.append('No Logo')
            except:
                naver_logo_list.append('Error')

            try:
                naver_footer_logo = soup.find_all('span', class_='footer_logo')
                if naver_footer_logo:
                    for tag in naver_footer_logo:
                        if tag.find('span', class_='blind') and '네이버' in tag.text: 
                            naver_footer_list.append('Find Naver Footer Logo in HTML')
                else:
                     naver_footer_list.append('No Logo')
            except:
                naver_footer_list.append('Error')

            try:
                kakao_logo = soup.find_all('span', class_='logo_kakao')
                if kakao_logo:
                    for tag in kakao_logo:
                        if tag.find('span', class_='ir_wa') and 'Kakao' in tag.text:
                            kakao_logo_list.append('Find Kakao Logo in HTML')
                else:
                    kakao_logo_list.append('No Logo')
            except:
                kakao_logo_list.append('Error')

            try:
                kakao_footer_logo = soup.find_all('a', class_='link_kakao')
                if kakao_footer_logo:
                    for tag in kakao_footer_logo:
                        if tag.get('href').startswith('http://kakaocorp.com') and 'Kakao' in tag.text :
                            kakao_footer_list.append("Find Kakao Footer Logo in HTML")
                else:
                    kakao_footer_list.append('No Logo')
            except:
                kakao_footer_list.append('Error')

        result['Status Code'] = pd.Series(status_code_list)
        result['End URL'] = pd.Series(reurl_list)
        result['Title'] = pd.Series(title_list)
        result['Naver Logo'] = pd.Series(naver_logo_list)
        result['Naver Footer Logo'] = pd.Series(naver_footer_list)
        result['Kakao Logo'] = pd.Series(kakao_logo_list)
        result['Kakao Footer Logo'] = pd.Series(kakao_footer_list)

        try:
            result.to_excel(target, index=False)
            print(
                f'{url}: Good {threading.current_thread().name} -[{count}/{urllen}]')
        except:
            print(
                f'{url}: Error {threading.current_thread().name} -[{count}/{urllen}]')
        count += 1
    print(
        f"--------------------{threading.current_thread().name} Complete--------------------")


# 각 파일에 대해 쓰레드 생성하고 시작
threads = []

for file in final_list:
    t = threading.Thread(target=Statusrun, args=(file,))
    threads.append(t)
    t.start()

# 모든 쓰레드가 끝날 때까지 기다림
for t in threads:
    t.join()
