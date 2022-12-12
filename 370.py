import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import csv
import numpy as np
import seaborn as sns
import matplotlib.ticker as ticker

df0 = pd.read_excel (r'370.xlsx',header=[3])
df0.drop(columns=['Transaction Type', 'Reference Number', 'Customer Vendor #','Inventory Balance', 'Transaction Date.1','Reference Number.1', 'Created By', 'Created Date', 'Inventory Quantity','Transaction Type.1', 'Created Time', 'Last Changed By', 'Last Changed Date','Receiving PO Number', 'Last Changed Time' ], inplace=True)
df0.rename(columns={'Customer/Vendor Name' : 'Customer','Non-Inventory Quantity': 'Qty', 'Transaction Date' : 'Date'}, inplace=True)
df0 = df0[df0.Customer != "TRANSFERS TO #372 J'VILLE"]
df0 = df0[df0.Customer != "TRANSFERS TO #374 SEYMOUR"]
df0 = df0[df0.Customer != "TRANSFERS TO #373 E-TOWN"]
df0 = df0[df0.Customer != "TRANSFERS TO #375 S'VILLE"]
df0 = df0[df0.Customer != "*** STORE TRANSFERS ***"]
df0 = df0[df0.Customer != "Beginning Balance"]
df0 = df0[df0.Customer != 'Net Activity']
df0 = df0[df0.Customer != 'Ending Balance']
df0 = df0[df0.Customer != 'VOID']
df0 = df0.dropna(how="all")

Gross = df0.Qty * df0.Price
df0['Gross'] = Gross.where(df0.Price == 'Qty', other=Gross)

Net = df0.Qty * df0.Cost 
df0['Net'] = Net.where(df0.Cost == 'Qty', other=Net)

Net = df0.Gross - df0.Net 
df0['Net'] = Net.where(df0.Gross == "Net", other=Net)

# Graph for total time span imported

Net_Gross270 = {
    'Gross' : df0['Gross'].sum(),
    'Net' : df0['Net'].sum()
}

data = Net_Gross270
names = list(data.keys())
values = list(data.values())

plt.title("370 Total Net and Gross for Import")
plt.bar(range(len(data)), values, tick_label=names)
plt.xticks(range(len(names)), names, rotation='vertical')
plt.show()

Total_Gross = df0['Gross'].sum()
Total_net = df0['Net'].sum() 

print('Total Gross:',(Total_Gross))
print('Total Net:',(Total_net))

# ------------------------------------

df0['Date'] = pd.to_datetime(df0['Date'], format='%y%m%d')
df0 = df0.groupby(df0['Date'].dt.to_period('m')).sum()
print(df0)