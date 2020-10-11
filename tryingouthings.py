import numpy as np
import pandas as pd
import plotly.graph_objects as go


df = pd.read_csv("data.csv")
df.head()
fig = go.Figure(data=[go.Table(header=dict(values=list(df.columns)),
                               cells=dict(values=[df.ItemID, df.SystemID, df.Buying, df.Selling]))])
fig.show()

