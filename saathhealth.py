# -*- coding: utf-8 -*-
"""Saathhealth.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XjdUXURx0JP_99txlB3WktOhkhUSkBPZ

Installing Libraries
"""

import json 
import pandas as pd 
from pandas.io.json import json_normalize
from collections import defaultdict
import matplotlib.pyplot as plt

"""Reading dataset and convert dataset to dataframe"""

df = pd.read_json(r'/content/SampleData.json')

df

"""
***Exploratory data analysis***
"""

df = df.transpose()

df.head()

"""Reindexing"""

df.reset_index(inplace=True)

"""**dividing timestamp by 1000 for changing into date format**

"""

for i in range(0,len(df['paid_at'])):
    df['paid_at'][i] = df['paid_at'][i]/1000
for i in range(0,len(df['paid_at'])):
    df['redeemed_at'][i] = df['redeemed_at'][i]/1000

df['time'] = df['paid_at']
df['time1'] = df['redeemed_at']

import datetime

"""**changing paid_at time to dd_mm_yyyy
make a new column called time and change time format to mm_yyyy**
"""

for i in range(0,len(df['paid_at'])):
    epoch_time = df['paid_at'][i]
  
    date_time = datetime.datetime.fromtimestamp( epoch_time )  
    df['paid_at'][i] = date_time.strftime("%d-%m-%Y")
    df['time'][i] = date_time.strftime("%m-%Y")

"""**changing redeemed_at time to dd_mm_yyyy make a new column called time1 and change time1 format to mm_yyyy**"""

for i in range(0,len(df['redeemed_at'])):
    epoch_time = df['redeemed_at'][i]
  
    date_time = datetime.datetime.fromtimestamp( epoch_time )  
    df['redeemed_at'][i] = date_time.strftime("%d-%m-%Y")
    df['time1'][i] = date_time.strftime("%m-%Y")

df.head()

"""checking how many we have null values"""

df.isna().sum()

df.info()

"""statistical analysis for data"""

df.describe()

df1 = df[['time1',"user_id",'items']]
grouped = df1.groupby(["time1","user_id"])
grouped.count()

"""**checking how many transactions happens at different months
by using function groyp by **
"""

df2 = df[['time1','items']]
grouped2 = df2.groupby(["time1"])
grouped2.count()

datf = pd.DataFrame(grouped2.count())
datf.reset_index(inplace=True)
datf

"""**Data visualization**

**we are making histogram plot of time vs number of transactions
for analysing  trends of company's Transaction**
"""

fig = plt.figure(figsize = (10, 5))
plt.bar(datf['time1'], datf["items"],
        width = 0.8, color = ['red', 'green'])
 
# naming the x-axis
plt.xlabel('months')
# naming the y-axis
plt.ylabel('number of transactions')
# plot title
plt.title('time vs number of transactions')
 
# function to show the plot
plt.show()

fig = plt.figure(figsize = (10, 5))
plt.plot(datf['time1'], datf["items"])
 
# naming the x-axis
plt.xlabel('months')
# naming the y-axis
plt.ylabel('number of transactions')
# plot title
plt.title('time vs number of transactions')
 
# function to show the plot
plt.show()

"""**finding no of unique user id for all months
for analysing how many different users we have at differet months**
"""

x = df.groupby('time1').user_id.nunique()
x = pd.DataFrame(x)
x.reset_index(inplace=True)
x

fig = plt.figure(figsize = (10, 5))
plt.bar(x['time1'], x["user_id"],
        width = 0.8, color = ['red', 'green'])
 
# naming the x-axis
plt.xlabel('months')
# naming the y-axis
plt.ylabel('number of user')
# plot title
plt.title('time vs number of users')
 
# function to show the plot
plt.show()

fig = plt.figure(figsize = (10, 5))
plt.plot(x['time1'], x["user_id"])
 
# naming the x-axis
plt.xlabel('months')
# naming the y-axis
plt.ylabel('number of user')
# plot title
plt.title('time vs number of users')
 
# function to show the plot
plt.show()

y= df.groupby('time1').k_user_id.nunique()
y = pd.DataFrame(y)
y.reset_index(inplace=True)
y

"""**finding no of unique k_user id for all months
for analysing how many different merchants we have at differet months**
"""

fig = plt.figure(figsize = (10, 5))
plt.bar(y['time1'], y["k_user_id"],
        width = 0.8, color = ['red', 'blue'])
 
# naming the x-axis
plt.xlabel('months')
# naming the y-axis
plt.ylabel('number of Merchants')
# plot title
plt.title('time vs number of Merchants')
 
# function to show the plot
plt.show()

fig = plt.figure(figsize = (10, 5))
plt.plot(y['time1'], y["k_user_id"],
        color = 'red')
 
# naming the x-axis
plt.xlabel('months')
# naming the y-axis
plt.ylabel('number of Merchants')
# plot title
plt.title('time vs number of Merchants')
 
# function to show the plot
plt.show()

column=df['time1'].unique()
column

df3 = pd.DataFrame(columns=column ,index =df["user_id"].unique())
df3

"""**making an overview of No. of transactions per User for the period between Nov 2018
to September 2019**

making dict of dict
deafult valu of all dict key is 0
"""

user_transaction = defaultdict(lambda: defaultdict(int))

for i in df.itertuples():
  user_transaction[i.user_id][i.time1]+=1

user_transaction

users_ids = df["user_id"].unique()

rows = []
for u in users_ids:
  temp = []
  for tim in column:
    temp.append(user_transaction[u][tim])
  rows.append(temp)

dataset = pd.DataFrame(rows, columns=column)

dataset.head()

dataset["user_id"] = users_ids
dataset.head()

first_column = dataset.pop('user_id')
dataset.insert(0, 'user_id', first_column)

dataset.head()

"""**making csv file from dataframe**"""

dataset.to_csv('user_transaction_redeem.csv')

""" **** Transactions that are done by each merchant for the 10 months period in
total**


"""

Merchants = df["k_user_id"].unique()
Merchants_transact = defaultdict(lambda: defaultdict(list))

for i in df.itertuples():
  Merchants_transact[i.k_user_id][i.time1].append(i.paid_amount)

rows = []
for m in Merchants:
  temp = []
  for tim in column:
    temp.append(Merchants_transact[m][tim])
  rows.append(temp)
Dataset3 = pd.DataFrame(rows, columns=column)
dr = Dataset3
Dataset3["merchant_id"] = Merchants

first_column = Dataset3.pop('merchant_id')
Dataset3.insert(0, 'merchant_id', first_column)
Dataset3

Dataset3.to_csv('k_user_Transactions.csv')

"""**count of Transactions that are done by each merchant for the 10 months period in total**"""

userIn = defaultdict(lambda: defaultdict(int))
for i in df.itertuples():
  userIn[i.k_user_id][i.time1]+=1

k_user = df["k_user_id"].unique()

rows = []
for user in k_user:
  cur = []
  for t in column:
    cur.append(userIn[user][t])
  rows.append(cur)

dataset4 = pd.DataFrame(rows, columns=column)

dataset4["k_user_id"] = k_user

first_column = dataset4.pop('k_user_id')
dataset4.insert(0, 'merchant_id', first_column)
dataset4

dataset4.to_csv("k_user_num_of_transaction.csv")

""" **Users who utilized the ???Merchant or K_user??? service in the 10 months period**"""

Merchants = df["k_user_id"].unique()
Merchants_transaction = defaultdict(lambda: defaultdict(list))

for i in df.itertuples():
  Merchants_transaction[i.k_user_id][i.time1].append(i.user_id)

rows = []
for m in Merchants:
  temp = []
  for tim in column:
    temp.append(Merchants_transaction[m][tim])
  rows.append(temp)

Dataset2 = pd.DataFrame(rows, columns=column)
Dataset2["merchant_id"] = Merchants

first_column = Dataset2.pop('merchant_id')
Dataset2.insert(0, 'merchant_id', first_column)

Dataset2

Dataset2.to_csv('K_user_with_users.csv')



for i in Dataset2:
   for j in range(2):
     print(Dataset2[i][j])
     print(len(Dataset2[i][j]))
     print(len(set(Dataset2[i][j])))

    
   break

for i in Dataset2:
   for j in range(2):
     Dataset2[i][j] = len(set(Dataset2[i][j]))

""" **count of Users who utilized the ???Merchant or K_user??? service in the 10 months period**"""

Dataset2["merchant_id"] = Merchants
first_column = Dataset2.pop('merchant_id')
Dataset2.insert(0, 'merchant_id', first_column)
Dataset2

Dataset2.to_csv('K_user_numberof_users.csv')