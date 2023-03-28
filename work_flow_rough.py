import re
import json
import time
import pandas as pd

# count the run time of a function
def timeit(func):
    def function(*params):
        start = time.time()
        ret = func(*params)
        runtime = time.time() - start
        print(runtime)
        return ret
    return function

# read json file and convert to csv file
with open("doi/doi_list copy.json", 'r') as fo:
    list_diction = json.load(fo)

csd_name = []
doi = []
for diction in list_diction:
    for key, value in diction.items():
        csd_name.append(key)
        doi.append(value)

df = pd.DataFrame({'csd_name': csd_name, 'doi': doi})
with open("doi_list.csv", 'w') as f:
    df.to_csv(f, index=False)

# read the csv file
with open("doi/doi_list.csv", 'r') as csv:
    df = pd.read_csv(csv)
    pd.set_option("display.max_rows", 5)

# create a df to collect each unique doi with the correspond first MOF name
doi_series_true = df.loc[df.doi.notnull()]
print(doi_series_true)

single_name = doi_series_true.groupby('doi').apply(lambda df: df.csd_name.iloc[0])
print(type(single_name))

with open("doi/digger_list.csv", "w") as f:
    single_name.to_csv(f)
    

"""remind that 10.1107 not shows the full content using 
https://doi.org/[doi] instead, using https://onlinelibrary.wiley.com/iucr/doi/[doi]"""

# shows how to combine groupby and read_csv to create a new dataFrame
with open("doi/digger_list.csv") as f:
    df = pd.read_csv(f)
    df = df.rename(columns={'0': "csd_name"})

df.to_csv("doi&csd_name.csv")

# filter specify doi prefix
with open("doi&csd_name.csv") as f:
    df = pd.read_csv(f, index_col=0)

mask = df.doi.str.contains("10.1039")
RSC_series = df[mask]
RSC_series.reset_index(drop=True)
print(RSC_series)
RSC_series.to_csv("RSCdoi&csd_name.csv")
