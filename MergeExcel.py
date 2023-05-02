import pandas as pd
import os

folder_path = "C:/Users/Mini1/Desktop/개발/Targetfile/" # 여러 개의 엑셀 파일이 저장된 폴더 경로
output_file = "C:/Users/Mini1/Desktop/개발/Targetfile/merged_file.xlsx" # 합쳐진 파일의 이름

files = [file for file in os.listdir(folder_path) if file.endswith('.xlsx')]

df_list = []
for file in files:
    df = pd.read_excel(os.path.join(folder_path, file))
    df_list.append(df)

merged_df = pd.concat(df_list)
merged_df.to_excel(output_file, index=False)