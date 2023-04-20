import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import asyncio

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

async def status_ham():
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        status_code_list.append(response.status_code)
        await asyncio.sleep(1)
    except:
        status_code_list.append('Error')
        await asyncio.sleep(1)

async def reurl_ham():
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        reurl_list.append(response.url)
        await asyncio.sleep(1)
    except:
        reurl_list.append('Error')
        await asyncio.sleep(1)

async def history_ham():
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        history_list.append(response.history)
        await asyncio.sleep(1)
    except:
        history_list.append('Error')
        await asyncio.sleep(1)

async def title_ham():
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        soup = BeautifulSoup(response.content, 'html.parser')
        title_list.append(soup.title.string)
        await asyncio.sleep(1)
    except:
        title_list.append('Error')
        await asyncio.sleep(1)

async def input_ham():
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        soup = BeautifulSoup(response.content, 'html.parser')
        input_list.append(soup.find_all('input'))
        await asyncio.sleep(1)
    except:
        input_list.append('Error')
        await asyncio.sleep(1)

async def form_ham():
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        soup = BeautifulSoup(response.content, 'html.parser')
        form_list.append(soup.find_all('form'))
        await asyncio.sleep(1)
    except:
        form_list.append('Error')
        await asyncio.sleep(1)

async def href_ham():
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        soup = BeautifulSoup(response.content, 'html.parser')
        href_list.append(soup.find_all('a'))
        await asyncio.sleep(1)
    except:
        href_list.append('Error')
        await asyncio.sleep(1)

async def main():
    await asyncio.gather(
        status_ham(),
        reurl_ham(),
        history_ham(),
        title_ham(),
        input_ham(),
        form_ham(),
        href_ham()
    )

for url in url_list:
    if not url.startswith('http'):
        url = 'http://' + url
    
    asyncio.run(main())
    
    time_list.append(datetime.now())
    result['Status Code'] = pd.Series(status_code_list)
    result['HTML Title'] = pd.Series(title_list)
    result['Redirection history'] = pd.Series(history_list)
    result['Input'] = pd.Series(input_list)
    result['Form'] = pd.Series(form_list)
    result['Href'] = pd.Series(href_list)
    result['End URL'] = pd.Series(reurl_list)
    result['Time'] = pd.Series(time_list)
        
    result.to_excel(filepath, index=False)

    print(f'{url} - [{count}/{urllen}]')
    print(f'{len(status_code_list)}, {len(title_list)}, {len(history_list)}, {len(input_list)}, {len(form_list)}, {len(href_list)}, {len(reurl_list)}')
    count += 1

print('--------------------엑셀작업 완료--------------------')

#        try:
#            response = requests.get(url, timeout=timeout, allow_redirects=True)
#            header_content_type_list.append(response.headers['Content-Type'])
#        except:
#            header_content_type_list.append('Error')    

#result['Content_type'] = pd.Series(header_content_type_list)