import pandas as pd
 
# read by default 1st sheet of an excel file
url = 'C:\\Users\\Administrator\\Downloads\\2023013068335ATL_IT.xlsx'
# for i in range(1,11):
#     df = pd.read_excel(url,'Part'+str(i))
#     df.to_csv('fbr_atl_2023_part_'+str(i))
# print(df.head())

df = pd.read_excel(url,'Part11')
df.to_csv('fbr_atl_2023_part_11.csv')