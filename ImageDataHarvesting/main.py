import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math


def main():
    file_name = "data_try_out.csv"
    data_frame = pd.read_csv(file_name, delimiter=";")
    analyzed_data = analyze_data(data_frame)
    visualize(analyzed_data)


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
        price_buying_item_id = sorted_data['ItemID'][ind]
        if math.isnan(price_buying):
            continue
        indexed_buying = (data_frame[data_frame.Buying.notnull()]).set_index(['ItemID', 'Buying'])
        sorted_data.loc[ind, 'Buying'] = indexed_buying['SystemID'][(price_buying_item_id, price_buying)]

    for ind in sorted_data.index:
        price_selling = sorted_data['Selling'][ind]
        if math.isnan(price_selling):
            continue
        indexed_selling = (data_frame[data_frame.Selling.notnull()]).set_index('Selling')
        sorted_data.loc[ind, 'Selling'] = indexed_selling['SystemID'][price_selling]
    return sorted_data


def visualize(data_frame):
    analyzed_data_sorted = data_frame.sort_values(['Buying', 'Selling'])
    analyzed_data_sorted.head()
    graph_constructor = go.Figure(data=[go.Table(header=dict(values=list(analyzed_data_sorted.columns)),
                                                 cells=dict(values=[analyzed_data_sorted.ItemID,
                                                                    analyzed_data_sorted.Buying,
                                                                    analyzed_data_sorted.Selling]))])
    graph_constructor.show()


if __name__ == '__main__':
    main()
