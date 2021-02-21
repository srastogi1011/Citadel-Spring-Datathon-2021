import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import scipy.stats as stats
import datetime
import os

# df = pd.read_csv('~/Documents/Citadel Datathons/Spring 2021 Datathon/arkansas-race-ethnicity-historical.csv')

def analyze(df, state):
    def return_date(string):
        string = str(string)
        return datetime.date(int(string[:4]), int(string[4:6]), int(string[6:])).strftime('%B %d, %Y')

    curr_df = df[['Date', 'Cases_Total', 'Cases_Asian', 'Cases_Black', 'Cases_White', 'Cases_Ethnicity_Hispanic']].iloc[::-1].set_index(df.index)
    curr_df['Date'] = curr_df['Date'].apply(return_date)
    curr_df['Pct_Asian'] = curr_df['Cases_Asian'] / curr_df['Cases_Total']
    curr_df['Pct_Black'] = curr_df['Cases_Black'] / curr_df['Cases_Total']
    curr_df['Pct_White'] = curr_df['Cases_White'] / curr_df['Cases_Total']
    curr_df['Pct_Hispanic'] = curr_df['Cases_Ethnicity_Hispanic'] / curr_df['Cases_Total']
    curr_df.drop(['Cases_Total', 'Cases_Asian', 'Cases_Black', 'Cases_White', 'Cases_Ethnicity_Hispanic'], inplace=True, axis=1)

    curr_df.plot(x='Date', y=['Pct_Asian', 'Pct_Black', 'Pct_White', 'Pct_Hispanic'])
    plt.suptitle('% of Cases by Race/Ethnicity in ' + state)
    plt.xlabel('Date')
    plt.ylabel('% of Cases')

    plt.savefig('Plots/' + state + '.png')

'''
df = pd.read_csv('~/Documents/Citadel Datathons/Spring 2021 Datathon/montana-history.csv')

mt_df = df[['date', 'death']].iloc[::-1].set_index(df.index)
mt_df = mt_df.iloc[51:] # 2020-04-26
mt_df.rename(columns={'death': 'mt_death'}, inplace=True)

joined_df = curr_df.set_index('date').join(mt_df.set_index('date'))

print(joined_df)


overall_pearson_r = curr_df.corr()
print(f"Pandas computed Pearson r: {overall_pearson_r}")
# out: Pandas computed Pearson r: 0.2058774513561943

r, p = stats.pearsonr(df.dropna()['S1_Joy'], df.dropna()['S2_Joy'])
print(f"Scipy computed Pearson r: {r} and p-value: {p}")
# out: Scipy computed Pearson r: 0.20587745135619354 and p-value: 3.7902989479463397e-51

# Compute rolling window synchrony
f, ax=plt.subplots(figsize=(7,3))
curr_df.rolling(window=30,center=True).median().plot(ax=ax)
ax.set(xlabel='Time',ylabel='Pearson r')
ax.set(title=f"Overall Pearson r = {np.round(overall_pearson_r,2)}")

plt.show()
'''

files = [f for f in os.listdir('.') if os.path.isfile(f)]

for f in files:
    filename, ext = os.path.splitext(f)
    state = filename.split('-')[0]
    if ext == '.csv':
        df = pd.read_csv(f)
        analyze(df, state)