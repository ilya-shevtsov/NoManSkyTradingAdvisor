import numpy as np
import pandas as pd
from tabulate import tabulate
df = pd.read_csv("data.csv", delimiter=";")
print(tabulate(df, headers='keys', tablefmt='psql'))

