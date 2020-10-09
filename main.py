import numpy as np
import pandas as pd
from tabulate import tabulate


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
    melted = pd.melt(data_frame, id_vars=['Item ID', 'System ID'], value_vars=['Buying', 'Selling'], var_name='Action')
    table = pd.pivot_table(melted, values='value', index=['Item ID', 'Action'], columns=['System ID'])
    print(table.fillna("-"))


if __name__ == '__main__':
    main()
