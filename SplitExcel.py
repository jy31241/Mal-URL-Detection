import pandas as pd

filename = "11"
filepath = pd.read_excel(f"C:/Users/Mini1/Desktop/개발/Targetfile/{filename}.xlsx")
newfile = "C:/Users/Mini1/Desktop/개발/Targetfile/"

n = 200 # 행 단위
m = (filepath.shape[0] - 1) // n + 1 # 파일 개수를 자동으로 계산

if filepath.shape[0] % n != 0: # 행이 n개로 나누어 떨어지지 않는 경우
    m += 1 # 파일 개수를 하나 늘림
for i in range(m):
    start = i * n # 시작 행
    end = (i + 1) * n # 끝 행
    filename = newfile +'target'+str(i + 1) + '.xlsx' # 파일 이름
    filepath.iloc[start:end].to_excel(filename, index=False) # 파일 저장