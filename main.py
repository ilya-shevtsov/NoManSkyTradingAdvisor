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
    sorted_data.dropna(subset=['Buying', 'Selling'], inplace=True)

    for ind in sorted_data.index:
        if sorted_data['Buying'][ind] > sorted_data['Selling'][ind]:
            sorted_data = sorted_data.drop([ind])
    sorted_data = sorted_data.reset_index(drop=True)
    for ind in sorted_data.index:
        price_buying = sorted_data['Buying'][ind]
        if math.isnan(price_buying):
            continue
        indexed_buying = (data_frame[data_frame.Buying.notnull()]).set_index('Buying')
        sorted_data.loc[ind, 'Buying'] = indexed_buying['SystemID'][price_buying]

    for ind in sorted_data.index:
        price_selling = sorted_data['Selling'][ind]
        if math.isnan(price_selling):
            continue
        indexed_selling = (data_frame[data_frame.Selling.notnull()]).set_index('Selling')
        sorted_data.loc[ind, 'Selling'] = indexed_selling['SystemID'][price_selling]
    return sorted_data


def visualize(data_frame):
    b = data_frame.sort_values(['Buying', 'Selling'])
    visualize_in_browser(b)


def visualize_in_browser(data):
    data.head()
    fig = go.Figure(data=[go.Table(header=dict(values=list(data.columns)),
                                   cells=dict(values=[data.ItemID, data.Buying,
                                                      data.Selling]))])
    fig.show()
    return fig


if __name__ == '__main__':
    main()
