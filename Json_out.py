import json
import pandas as pd

read_data = []

with open('C:/Users/Mini1/Desktop/개발/Json/11.json', 'r', encoding='UTF8') as f:
    for line in f:
        read_data.append(json.loads(line))

extracted_data = []
for item in read_data:
    extracted_data.append({
        'ip_address': item['ip_address'],
        'title': item['title'],
    })

df = pd.DataFrame(extracted_data)
df.to_excel('C:/Users/Mini1/Desktop/개발/Json/output.xlsx', index=False)