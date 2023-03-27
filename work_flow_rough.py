import re
import json
import time
import pandas as pd

def timeit(func):
    def function(*params):
        start = time.time()
        ret = func(*params)
        runtime = time.time() - start
        print(runtime)
        return ret
    return function


# with open("doi_list copy.json", 'r') as fo:
#     list_diction = json.load(fo)

# csd_name = []
# doi = []
# for diction in list_diction:
#     for key, value in diction.items():
#         csd_name.append(key)
#         doi.append(value)

# df = pd.DataFrame({'csd_name': csd_name, 'doi': doi})
# with open("doi_list.csv", 'w') as f:
#     df.to_csv(f, index=False)

# with open("doi_list.csv", 'r') as csv:
#     df = pd.read_csv(csv)
#     pd.set_option("display.max_rows", 5)

# doi_series_true = df.loc[df.doi.notnull()]
# print(doi_series_true)
# doi_number = doi_series_true.doi.unique()
# print(len(doi_number))

# doi_csd_name = doi_series_true.groupby(['doi']).size()
# print(doi_csd_name)

# single_name = doi_series_true.groupby('doi').apply(lambda df: df.csd_name.iloc[0])
# print(type(single_name))

# with open("digger_list.csv", "w") as f:
#     single_name.to_csv(f)
    

"""remind that 10.1107 not shows the full content using 
https://doi.org/[doi] instead, using https://onlinelibrary.wiley.com/iucr/doi/[doi]"""


with open("doi/digger_list.csv") as csv:
    series = pd.read_csv(csv)

prefix_1006 = series.doi.map(lambda prefix: '10.1006' in prefix).sum()
# print(prefix_1006)

series = series[~series.doi.str.startswith(('10.1006','10.1071', '10.1055', '10.1080'))]



# print(series)

prefixes = series.doi.str.extract(r'(\d+\.\d+)')[0]
group = series.groupby(prefixes).size()
print(group)

