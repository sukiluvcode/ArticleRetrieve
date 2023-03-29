"""To get the file path"""
import os
import time
import pandas as pd
from downloader.articledownloader import ArticleDownloader

def download(doi, file_name):
    """download the file with given doi"""
    downloader = ArticleDownloader()
    cwd = os.getcwd()
    file_path = os.path.join(cwd, f"Publication/{file_name}.html")
    my_file = open(file_path, 'wb')
    downloader.get_html_from_doi(doi=doi, writefile=my_file, mode="rsc")

with open("doi/RSCdoi&csd_name.csv", encoding="utf-8") as f:
    RSC = pd.read_csv(f, index_col=0)

doi_list = list(RSC.doi)
name_list = list(RSC.csd_name)

for i in range(5,100):
    download(doi_list[i], name_list[i])
    time.sleep(2)
