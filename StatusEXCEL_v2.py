import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import sys

filepath = 'C:/Users/Mini1/Desktop/개발/Targetfile/230402_query_iptime(0401~0420).xlsx'
result = pd.read_excel(filepath)

url_list = result['URL'].tolist()
status_code_list = []
title_list = []
history_list = []
#header_content_type_list = []
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
            response = requests.get(url, timeout=timeout, allow_redirects=True)
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
            
#        try:
#            response = requests.get(url, timeout=timeout, allow_redirects=True)
#            header_content_type_list.append(response.headers['Content-Type'])
#        except:
#            header_content_type_list.append('Error')                            

        time_list.append(datetime.now())
        result['Status Code'] = pd.Series(status_code_list)
        result['HTML Title'] = pd.Series(title_list)
        result['Redirection history'] = pd.Series(history_list)
        result['Input'] = pd.Series(input_list)
        result['Form'] = pd.Series(form_list)
        result['Href'] = pd.Series(href_list)
        result['End URL'] = pd.Series(reurl_list)
        result['Time'] = pd.Series(time_list)
        #result['Content_type'] = pd.Series(header_content_type_list)
        result.to_excel(filepath, index=False)

        print(f'{url} - [{count}/{urllen}]')
        print(f'{len(status_code_list)}, {len(title_list)}, {len(history_list)}, {len(input_list)}, {len(form_list)}, {len(href_list)}, {len(reurl_list)}')
        count += 1

print('--------------------엑셀작업 완료--------------------')
