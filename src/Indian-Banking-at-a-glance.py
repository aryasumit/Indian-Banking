# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 08:40:09 2020

@author: Arya Sumit
"""
# Import libraries
import os
import pandas as pd

# Create raw data path
Raw_data_path = "C:\DATA\Portfolio\Indian Banking\Indian-Banking\data"

"""
Import data sets 
"""
# Import assets and liabilities data set
assets_liabilities = pd.read_excel(os.path.join(Raw_data_path,"assets_liabilities.xlsx"), sheet_name="ASSETS")
bank_type = pd.read_excel(os.path.join(Raw_data_path,"bank_type.xlsx"), sheet_name="bank_type")

"""
Data cleaning
"""
### Clean assets and liabilities data set 
# Remove nan rows on the top and bottom
assets_liabilities = assets_liabilities[assets_liabilities['Unnamed: 1'].notnull()]
# Set the first row as header
new_header = assets_liabilities.iloc[0]
new_header = new_header.str.strip()
assets_liabilities = assets_liabilities[1:]
assets_liabilities.columns = new_header
# Fill year value for null rows
assets_liabilities['Year'].fillna(method='ffill', inplace=True)
# Get the bank type
assets_liabilities = assets_liabilities.reset_index()
assets_liabilities = assets_liabilities.merge(bank_type, left_on='Banks', right_on='Bank type', how = 'outer')
assets_liabilities.sort_values(by='index', inplace=True)
assets_liabilities['Bank type'].fillna(method='bfill', inplace=True)

"""

"""

assets_liabilities.head(10)
