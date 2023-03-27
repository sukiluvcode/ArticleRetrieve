import pandas as pd

with open("doi/digger_list.csv") as f:
    df = pd.read_csv(f)
    df = df.rename(columns={'0': "csd_name"})

df.to_csv("doi&csd_name.csv")