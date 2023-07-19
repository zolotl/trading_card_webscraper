import pandas as pd
from datetime import date

product_name = "peptrojepotje"
price = 1200

csv_path = "results\\test.csv"

df = pd.read_csv(csv_path)

curr_date = date.today().strftime("%Y-%m-%d")
print(curr_date in df['date'].values)
if curr_date in df['date'].values:
    df.loc[df['date'] == curr_date, product_name] = price
else:
    df.loc[len(df)] = curr_date
    df.loc[df['date'] == curr_date, product_name] = price

df.to_csv(csv_path, index=False)
