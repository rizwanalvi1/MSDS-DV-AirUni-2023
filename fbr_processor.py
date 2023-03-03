import pandas as pd

# Define the input and output file paths
input_file = '2023030118335ATL_IT.xlsx'
output_folder = 'fbr/'

# Read the Excel file
xlsx = pd.read_excel(input_file, sheet_name=None)

# Loop through all sheets in the Excel file and convert them to CSV
for sheet_name, sheet_data in xlsx.items():
    csv_file = output_folder + sheet_name + '.csv'
    sheet_data.to_csv(csv_file, index=False)


