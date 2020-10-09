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
    print(tabulate(data_frame, headers='keys', tablefmt='psql'))


if __name__ == '__main__':
    main()

