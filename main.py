import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math


def main():
    file_name = "data.csv"
    data_frame = read_data(file_name)
    analyzed_data = analyze_data(data_frame)
    visualize(analyzed_data)


def read_data(file_name):
    data_frame = pd.read_csv(file_name, delimiter=";")
    return data_frame


def analyze_data(data_frame):
    data_frame = data_frame.replace(0, np.NaN)
    sorted_data = data_frame.groupby('ItemID').agg({'Buying': min, 'Selling': max}).reset_index()
    for ind in sorted_data.index:
        price = sorted_data['Buying'][ind]
        if math.isnan(price):
            continue
        indexed = (data_frame[data_frame.Buying.notnull()]).set_index('Buying')
        sorted_data.loc[ind, 'Buying'] = indexed['SystemID'][price]
    print(sorted_data)
    return sorted_data


def visualize(data_frame):
    visualize_in_browser(data_frame)


def visualize_in_browser(data):
    data.head()
    fig = go.Figure(data=[go.Table(header=dict(values=list(data.columns)),
                                   cells=dict(values=[data.ItemID, data.Buying,
                                                      data.Selling]))])
    fig.show()
    return fig


if __name__ == '__main__':
    main()
