import pandas as pd

df = pd.read_csv('pmsearch_jd_jx.csv')

print(df["详情页标题"], df["页面网址"])
