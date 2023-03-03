from tabula import read_pdf
from tabulate import tabulate
import pandas as pd
 
# df = read_pdf("FBRTaxAnalysis.pdf",pages="all") 
# df = read_pdf("FBRTaxAnalysis.pdf",pages=10) 
# df = read_pdf("TaxpayersDirectory2018/TaxpayersDirectory2018.pdf",pages='4-15000', encoding = 'cp1252')
df = read_pdf("TaxpayersDirectory2018/TaxpayersDirectory2018.pdf",pages='15001-30000', encoding = 'cp1252')
# , encoding = 'unicode_escape'

# for i in range(10, 22):
    # len(df[i])
combined_df = pd.DataFrame()
chunks = []
# for d in df:
#     print(d)
#     print(d.head())
#     combined_df = pd.concat(combined_df, d, ignore_index=True)
for i in range(len(df)):
    # print(len(df[i]))
    # chunks.append(tabulate(df[i]))
    chunks.append(df[i])
    # print(df[i].head())
    # combined_df = pd.concat(combined_df, df[i])

combined_df = pd.concat(chunks, ignore_index=True)
# print(tabulate(combined_df, showindex=False, headers=['Sr.', 'Taxpayer Name', 'Registration No.','Tax Paid']))
# combined_df = combined_df.reset_index(drop=True)
# combined_df.to_csv('fb_4-15K.csv')
combined_df.to_csv('fb_15K-30K.csv')

# df2 = pd.read_csv(tabulate(combined_df, showindex=False, headers=['City', 'Tax Collected (Rs.)']))
# df2.to_csv('test.csv')
# print(df.head())
# print(len(combined_df))


# print(tabulate(df[1]))
