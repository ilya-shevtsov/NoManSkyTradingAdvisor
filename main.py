import numpy as np
import pandas as pd
import plotly.graph_objects as go


def main():
    file_name = "data.csv"
    data_frame = read_data(file_name)
    analyzed_data = analyze_data(data_frame)
    visualize(analyzed_data)


def read_data(file_name):
    data_frame = pd.read_csv(file_name, delimiter=";")
    return data_frame


def analyze_data(data_frame):
    return data_frame


def visualize(data_frame):
    data_frame.head()
    fig = go.Figure(data=[go.Table(header=dict(values=list(data_frame.columns)),
                                   cells=dict(values=[data_frame.ItemID, data_frame.SystemID, data_frame.Buying,
                                                      data_frame.Selling]))])
    fig.show()


if __name__ == '__main__':
    main()
