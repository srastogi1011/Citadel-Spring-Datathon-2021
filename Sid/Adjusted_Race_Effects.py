import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import scipy.stats as stats
import datetime
import os

race_breakdown_df = pd.read_csv('~/Documents/Citadel Datathons/Spring 2021 Datathon/Sid/Racial Breakdown/racial_breakdown_by_state.csv')
race_breakdown_df['Location'] = race_breakdown_df['Location'].str.lower()

def analyze(df, state):
    def return_date(string):
        string = str(string)
        return datetime.date(int(string[:4]), int(string[4:6]), int(string[6:])).strftime('%B %d, %Y')
    
    asian_pct_in_state = race_breakdown_df.loc[race_breakdown_df['Location'] == state, 'Asian'].item()
    black_pct_in_state = race_breakdown_df.loc[race_breakdown_df['Location'] == state, 'Black'].item()
    white_pct_in_state = race_breakdown_df.loc[race_breakdown_df['Location'] == state, 'White'].item()
    hispanic_pct_in_state = race_breakdown_df.loc[race_breakdown_df['Location'] == state, 'Hispanic'].item()

    curr_df = df[['Date', 'Cases_Total', 'Cases_Asian', 'Cases_Black', 'Cases_White', 'Cases_Ethnicity_Hispanic']].iloc[::-1].set_index(df.index)
    curr_df['Date'] = curr_df['Date'].apply(return_date)
    curr_df['Pct_Asian'] = (curr_df['Cases_Asian'] / curr_df['Cases_Total']) / asian_pct_in_state * 100
    curr_df['Pct_Black'] = curr_df['Cases_Black'] / curr_df['Cases_Total'] / black_pct_in_state * 100
    curr_df['Pct_White'] = curr_df['Cases_White'] / curr_df['Cases_Total'] / white_pct_in_state * 100
    curr_df['Pct_Hispanic'] = curr_df['Cases_Ethnicity_Hispanic'] / curr_df['Cases_Total'] / hispanic_pct_in_state * 100
    curr_df.drop(['Cases_Total', 'Cases_Asian', 'Cases_Black', 'Cases_White', 'Cases_Ethnicity_Hispanic'], inplace=True, axis=1)

    curr_df.plot(x='Date', y=['Pct_Asian', 'Pct_Black', 'Pct_White', 'Pct_Hispanic'])
    plt.suptitle('% of Cases by Race/Ethnicity in ' + state.capitalize() + ' (Adjusted)')
    plt.xlabel('Date')
    plt.ylabel('% of Cases Relative to Expectation')
    plt.xticks(rotation = 45)
    plt.tight_layout()


    plt.savefig('Adjusted Plots/' + state.capitalize() + '.png')


files = [f for f in os.listdir('.') if os.path.isfile(f)]

for f in files:
    filename, ext = os.path.splitext(f)
    state = filename.split('-')[0]
    if ext == '.csv':
        df = pd.read_csv(f)
        analyze(df, state)