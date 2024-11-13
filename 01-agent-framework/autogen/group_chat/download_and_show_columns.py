# filename: download_and_show_columns.py
import pandas as pd

# 데이터셋 URL
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"

# 데이터셋 다운로드
data = pd.read_csv(url)

# 데이터셋의 열(column) 출력
print(data.columns.tolist())