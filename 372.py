import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import csv
import numpy as np
import seaborn as sns
import matplotlib.ticker as ticker

df1 = pd.read_excel (r'372.xlsx',header=[3])
df1.drop(columns=['Transaction Type', 'Reference Number', 'Customer Vendor #','Inventory Balance', 'Transaction Date.1','Reference Number.1', 'Created By', 'Created Date', 'Inventory Quantity','Transaction Type.1', 'Created Time', 'Last Changed By', 'Last Changed Date','Receiving PO Number', 'Last Changed Time' ], inplace=True)
df1.rename(columns={'Customer/Vendor Name' : 'Customer','Non-Inventory Quantity': 'Qty', 'Transaction Date' : 'Date'}, inplace=True)
df1 = df1[df1.Customer != "TRANSFERS TO #372 J'VILLE"]
df1 = df1[df1.Customer != "TRANSFERS TO #374 SEYMOUR"]
df1 = df1[df1.Customer != "TRANSFERS TO #373 E-TOWN"]
df1 = df1[df1.Customer != "TRANSFERS TO #375 S'VILLE"]
df1 = df1[df1.Customer != "*** STORE TRANSFERS ***"]
df1 = df1[df1.Customer != "Beginning Balance"]
df1 = df1[df1.Customer != 'Net Activity']
df1 = df1[df1.Customer != 'Ending Balance']
df1 = df1[df1.Customer != 'VOID']
df1 = df1.dropna(how="all")

Gross = df1.Qty * df1.Price
df1['Gross'] = Gross.where(df1.Price == 'Qty', other=Gross)

Net = df1.Qty * df1.Cost 
df1['Net'] = Net.where(df1.Cost == 'Qty', other=Net)

Net = df1.Gross - df1.Net 
df1['Net'] = Net.where(df1.Gross == "Net", other=Net)

# Graph for total time span imported

Net_Gross272 = {
    'Gross' : df1['Gross'].sum(),
    'Net' : df1['Net'].sum()
}

data = Net_Gross272
names = list(data.keys())
values = list(data.values())

plt.bar(range(len(data)), values, tick_label=names)
plt.xticks(range(len(names)), names, rotation='vertical')
plt.show()

Total_Gross = df1['Gross'].sum()
Total_net = df1['Net'].sum() 

print('Total Gross:',(Total_Gross))
print('Total Net:',(Total_net))


# ----------------------------------------

df1['Date'] = pd.to_datetime(df1['Date'], format='%y%m%d')
df1 = df1.groupby(df1['Date'].dt.to_period('m')).sum()
print(df1)