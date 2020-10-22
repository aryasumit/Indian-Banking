# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 08:40:09 2020

@author: Arya Sumit
"""
# Import libraries
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Create raw data path
Raw_data_path = "C:\DATA\Portfolio\Indian Banking\Indian-Banking\data"

"""
Import data sets 
"""
# Import assets and liabilities data set
assets = pd.read_excel(os.path.join(Raw_data_path,"assets_liabilities.xlsx"), sheet_name="ASSETS")
liabilities = pd.read_excel(os.path.join(Raw_data_path,"assets_liabilities.xlsx"), sheet_name="LIABILITIES")
bank_type = pd.read_excel(os.path.join(Raw_data_path,"bank_type.xlsx"), sheet_name="bank_type")

"""
Data cleaning
"""

x=liabilities
### Clean assets and liabilities data set 
def clean_data(x):
    global cln_data
    # Remove nan rows on the top and bottom
    x = x[x['Unnamed: 1'].notnull()]
    # Set the first row as header
    new_header = x.iloc[0]
    new_header = new_header.str.strip()
    x = x[1:]
    x.columns = new_header
    # Fill year value for null rows
    x['Year']= x['Year'].fillna(method='ffill')
    # Get the bank type
    x = x.reset_index()
    x = x.merge(bank_type, left_on='Banks', right_on='Bank type', how = 'outer')
    x.sort_values(by='index', inplace=True)
    x['Bank type'].fillna(method='bfill', inplace=True)
    # Exclude rows with sub-totals
    x = x.merge(bank_type, left_on='Banks', right_on='Bank type', how = 'outer')
    x.sort_values(by='index', inplace=True)
    x = x[x['Bank type_y'].isnull()]
    
    x['Banks'].replace(regex=['LTD.'], value='', inplace=True)
    x['Banks'].replace(regex=['LTD'], value='', inplace=True)
    x['Banks'].replace(regex=[','], value='', inplace=True)
    x['Banks'].replace(regex=['PJSC'], value='', inplace=True)
    x['Banks'].replace(regex=['NATIONAL ASSOCIATION'], value='', inplace=True)
    x['Banks'].replace(regex=['N.A.'], value='', inplace=True)
    x['Banks'].replace(regex=['N.A'], value='', inplace=True)
    x['Banks'].replace(regex=['CO.'], value='', inplace=True)
    x['Banks'].replace(regex=[' CORPORATE AND INVESTMENT BANK'], value='', inplace=True)
    x['Banks'].replace(regex=['JPMORGAN'], value='JP MORGAN', inplace=True)
    x['Banks'].replace(regex=['RBL BANK LIMITED'], value='RBL', inplace=True)
    x['Banks'].replace(regex=['& JAIPUR'], value='AND JAIPUR', inplace=True)
    x['Banks'].replace(regex=['CORP.'], value='', inplace=True)
    x['Banks'].replace(regex=['LIMITED'], value='', inplace=True)
    x['Banks'].replace(regex=['MUFG Bank Ltd'], value='MUFG BANK', inplace=True)
    x['Banks'].replace(regex=['THE DHANALAKSHMI BANK'], value='DHANALAKSHMI BANK', inplace=True)
    
    x['Banks']=x['Banks'].str.strip()
    
    cln_data = x
    
    
clean_data(assets)
cln_assets = cln_data
clean_data(liabilities)
cln_liabilities = cln_data


    

"""
Advances
"""
Adv_2019 = cln_assets[cln_assets['Year']==2019]
# Adv_2019['7.     Advances'] = Adv_2019['7.     Advances'].astype(float)
Adv_2019['7.     Advances'] = pd.to_numeric(Adv_2019['7.     Advances'] ,errors='coerce')
Adv_2019_bank_type = Adv_2019.groupby(['Bank type_x'])['7.     Advances'].agg('sum')
Adv_2019_bank_type = pd.DataFrame(Adv_2019_bank_type)
Adv_2019_bank_type.reset_index(inplace=True)

sns.set_style(style="whitegrid")

penguins = sns.load_dataset("penguins")

# Draw a nested barplot by species and sex
plt.figure(figsize=(12,12)) 
g = sns.catplot(
    data=Adv_2019_bank_type, kind="bar",
    x="Bank type_x", y="7.     Advances",
    ci="sd", palette="dark", alpha=.9, height=6
)
g.set_xticklabels(g.get_xticklabels(), rotation=40, ha="right")
g.despine(left=True)
g.set_axis_labels("", "Advances")
plt.show()
g.legend.set_title("")

Adv_2019_bank_type.sort_values( by = '7.     Advances', inplace=True,  ascending=False)
ax = sns.barplot(x="Bank type_x", y= "7.     Advances", data=Adv_2019_bank_type)
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
ax.set(xlabel='Bank Type', ylabel='Advances', title='Advances by bank type')
plt.tight_layout()
plt.show()



df = pd.DataFrame({'mass': [0.330, 4.87 , 5.97],
                   'radius': [2439.7, 6051.8, 6378.1]},
                  index=['Mercury', 'Venus', 'Earth'])

plot = Adv_2019_bank_type.plot.pie(y='7.     Advances', figsize=(5, 5))


fig, ax = plt.subplots()

size = 0.3
# vals = np.array([[60., 32.], [37., 40.], [29., 10.]])
vals = cln_assets['7.     Advances']

cmap = plt.get_cmap("tab20c")
outer_colors = cmap(np.arange(3)*4)
inner_colors = cmap([1, 2, 5, 6, 9, 10])

ax.pie(vals.sum(axis=1), radius=1, colors=outer_colors,
       wedgeprops=dict(width=size, edgecolor='w'))

ax.pie(vals.flatten(), radius=1-size, colors=inner_colors,
       wedgeprops=dict(width=size, edgecolor='w'))

ax.set(aspect="equal", title='Pie plot with `ax.pie`')
plt.show()


