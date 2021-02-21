import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import scipy.stats as stats

df = pd.read_csv('~/Documents/Citadel Datathons/Spring 2021 Datathon/Sid/Datathon Materials/3_covidtracking/alabama-history.csv')

def returnGrade(letter):
    dataGrades = {'A': 3, 'B': 2, 'C': 1, 'F': 0}
    return dataGrades[letter]

df['dataQualityGrade'] = df['dataQualityGrade'].fillna('F')
df['dataQualityAsNum'] = df.apply(lambda row: returnGrade(row.dataQualityGrade), axis = 1)

df = df.dropna(axis=1,how='all')

df = df[['date', 'death', 'deathConfirmed', 'deathIncrease', 'positive', 'positiveIncrease', 'totalTestResults', 'totalTestResultsIncrease', 'dataQualityAsNum']]

print(df.head())

corrMatrix = df.corr()
sn.heatmap(corrMatrix, annot=True)
plt.tight_layout()
plt.savefig('CorrMatrix.png')

'''
al_df = df[['dataQualityGrade', 'positive']].iloc[::-1].set_index(df.index)

print(al_df)

overall_pearson_r = al_df.corr()
print(f"Pandas computed Pearson r: {overall_pearson_r}")
# out: Pandas computed Pearson r: 0.2058774513561943

r, p = stats.pearsonr(df.dropna()['S1_Joy'], df.dropna()['S2_Joy'])
print(f"Scipy computed Pearson r: {r} and p-value: {p}")
# out: Scipy computed Pearson r: 0.20587745135619354 and p-value: 3.7902989479463397e-51

# Compute rolling window synchrony
f, ax=plt.subplots(figsize=(7,3))
al_df.rolling(window=30,center=True).median().plot(ax=ax)
ax.set(xlabel='Time',ylabel='Pearson r')
ax.set(title=f"Overall Pearson r = {np.round(overall_pearson_r,2)}")

plt.savefig('alabama.png')
'''