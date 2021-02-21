import pandas as pd
import plotly.express as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from numpy import cov
import statistics 






def updateAvailabilityScores():
    StateNames = ["AR","CO","FL","MI","MT","NY","OH","OK","VT","WA"]
    CatagoriesThatMatter = ["death","hospitalizedCurrently","inIcuCurrently","onVentilatorCurrently","recovered","LTC_Data_Available"]
    for state in StateNames:
        df = pd.read_csv("StateData/" + state + ".csv")
        scores = []
        for row in df.itertuples():
            score = 0
            for col in df.columns:
                if col in CatagoriesThatMatter:
                    if str(getattr(row, col)) != "nan":
                        score += 1
            scores.append(score/len(CatagoriesThatMatter))
        scores.reverse()



        fig = plt.scatter(x=[i for i in range(len(scores))], y=scores)
        fig.update_layout(xaxis=dict(rangeslider=dict(visible=True)))
        fig.show()
        scores.reverse()
        df["Score"] = scores
        df.to_csv("StateData/" + state + ".csv")

def includeNewData():
    state = "WA"
    df = pd.read_csv("StateData/" + state + ".csv")
    an_array = np.empty(403)
    an_array[:] = np.NaN
    for i in range(0):
        an_array[i] = 1
    print(an_array)
    df["LTC_Data_Available"] = an_array
    df.to_csv("StateData/" + state + ".csv")

def visualizeData():
    StateNames = ["AR","CO","FL","MI","MT","NY","OH","OK","VT","WA"]
    covs = []
    totDeaths = []
    totScores = []
    for state in StateNames:
        df = pd.read_csv("StateData/" + state + ".csv")
        deaths = df["death"].tolist()
        deathIncrease = df["deathIncrease"].tolist()
        scores = df["Score"].tolist()
        index = df["Unnamed: 0"].tolist()
        index.reverse()

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=index, y=deaths, name="Cumulative Deaths"),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=index, y=scores, name="Availability Score"),
            secondary_y=True,
        )
        fig.update_yaxes(range=[0, 1], secondary_y=True)
        # Add figure title
        fig.update_layout(
            title_text=state
        )
        # Set x-axis title
        fig.update_xaxes(title_text="Days Since First Infection")
        fig.update_layout(
        font=dict(
        size=24)
        )
        fig.show()

        fig = plt.histogram(df, x="deathIncrease")
        #fig.show()

        data1 = deathIncrease
        data2 = scores
        # calculate covariance matrix
        #covariance = cov(data1, data2)
        cov = 0
        for i in range(len(deaths)):
            cov += (deathIncrease[i] - statistics.median(deathIncrease)) * (scores[i] - statistics.median(scores)) * (1/(len(deathIncrease)-1))
            totDeaths.append(deathIncrease[i])
            totScores.append(scores[i])
        print(str(cov) + "  " + state)
        covs.append(cov)

    cov = 0
    print(totDeaths)
    for i in range(len(totDeaths)):
        cov += (totDeaths[i] - statistics.median(totDeaths)) * (totScores[i] - statistics.median(totScores)) * (1/(len(totDeaths)-1))
    print(cov)
    


    fig = plt.choropleth(locations=StateNames, locationmode="USA-states", color=covs, scope="usa",title="Covariance of Daily Availability Score and Deaths")
    fig.update_layout(
    font=dict(
    size=24)
    )
    fig.show()

#updateAvailabilityScores()
#includeNewData()
visualizeData()