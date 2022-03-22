import openpyxl
import pandas as pd

df = pd.read_excel(r'C:\Users\SSY\Desktop\work\intern\insta_scraping\excel\follower_list_1.xlsx', sheet_name='Sheet2')
tot_follower = len(df.index)
print(tot_follower)

nan_val = float("NaN")
df.replace("", nan_val, inplace=True)

df['Full Name'] = df['Full Name'].str.replace(r'\W', "")
df.dropna(subset = ["Full Name"], inplace=True)