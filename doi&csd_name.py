import pandas as pd

with open("doi&csd_name.csv") as f:
    df = pd.read_csv(f, index_col=0)

mask = df.doi.str.contains("10.1039")
RSC_series = df[mask]
RSC_series.reset_index(drop=True)
print(RSC_series)
RSC_series.to_csv("RSCdoi&csd_name.csv")