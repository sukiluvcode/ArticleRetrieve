"""
retrieve articles from elsevier, springer nature rsc, not include acs specifically.
recommand set interval to 1s for each retrieve isntance call.
wiley and aaas articles are hard to download, they are needs cookies.
"""
import os
import re
import time
import logging
import subprocess
import random
import pandas as pd
from downloader.articledownloader import ArticleDownloader
from config.config import get_config


els_api_key = get_config("apikey.config", "apikey", "els_api_key")
springer_api_key = get_config("apikey.config", "apikey", "springer_api_key")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# anti anti crawler
agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"
]

class Retrieve:
    """
    separate doi download stream into different chunks
    """
    prefix = {"springer": ["10.1007", "10.1134", "10.1023", "10.1038"],
              "elsevier": ["10.1016"],
              "wiley": ["10.1002", "10.1107"],
              "rsc": ["10.1039"],
              "acs": ["10.1021"],
              "aaas": ["10.1126"]}

    def __init__(self, doi, download_loc):
        self.doi = doi
        self.download_loc = download_loc  # refers to the download directory

    def recognizer(self):
        _pattern = r"10\.\d{4}"
        match = re.search(_pattern, self.doi)
        match_publisher = None

        if match is not None:
            for publisher in self.prefix:
                if match.group(0) in self.prefix[publisher]:
                    match_publisher = publisher

        if match_publisher:
            return match_publisher
        else:
            logger.info(f"sorry, we do not provide access to {self.doi}!")
            return None

    def download(self, file_name):
        """download the article from specific publisher"""
        publisher = self.recognizer()

        if publisher is None:
            return None

        if publisher == "acs":
            logger.info(
                f"sorry, scrawler is forbidden in {publisher}")
            return None

        if publisher == "aaas":
            base_url = "https://doi.org/"
            url = base_url + self.doi
            abs_file_path = f"{os.path.join(self.download_loc, file_name)}.html"
            curl(random.choice(agent_list), url, abs_file_path)
            if validation(abs_file_path):
                logger.info(f"successfully download {self.doi} from {publisher}, located at {os.path.join(self.download_loc, file_name)}.html")
            else:
               logger.info(f"sorry, {os.path.join(self.download_loc, file_name)}.html is empty, something went wrong") 
            return None  

        if publisher == "elsevier":
            downloader = ArticleDownloader(els_api_key=els_api_key)
            my_file = open(f"{self.download_loc}/{file_name}.xml", 'wb')
            downloader.get_xml_from_doi(
                doi=self.doi, writefile=my_file, mode=publisher)
            my_file.close()
            if validation(f"{os.path.join(self.download_loc, file_name)}.xml"):
                logger.info(f"successfully download {self.doi} from {publisher}, located at {os.path.join(self.download_loc, file_name)}.xml")
            else:
                logger.info(f"sorry, {os.path.join(self.download_loc, file_name)}.xml is empty, something went wrong")
            return None 

        if publisher == "wiley":
            base_url = "https://onlinelibrary.wiley.com/doi/full-xml/"
            url = base_url + self.doi
            abs_file_path = f"{os.path.join(self.download_loc, file_name)}.xml"
            curl(random.choice(agent_list), url, abs_file_path)
            if validation(abs_file_path):
                logger.info(f"successfully download {self.doi} from {publisher}, located at {os.path.join(self.download_loc, file_name)}.xml")
            else:
               logger.info(f"sorry, {os.path.join(self.download_loc, file_name)}.xml is empty, something went wrong") 
            return None 

        if publisher == 'springer':
            downloader = ArticleDownloader(springer_api_key=springer_api_key)
            my_file = open(f"{self.download_loc}/{file_name}.html", 'wb')
            downloader.get_html_from_doi(
            doi=self.doi, writefile=my_file, mode=publisher)
            my_file.close()
            if validation(f"{os.path.join(self.download_loc, file_name)}.html"):
                logger.info(f"successfully download {self.doi} from {publisher}, located at {os.path.join(self.download_loc, file_name)}.html")
            else:
                logger.info(f"sorry, {os.path.join(self.download_loc, file_name)}.html is empty, something went wrong") 
            return None 

        downloader = ArticleDownloader()
        my_file = open(f"{self.download_loc}/{file_name}.html", 'wb')
        downloader.get_html_from_doi(
            doi=self.doi, writefile=my_file, mode=publisher)
        my_file.close()
        if validation(f"{os.path.join(self.download_loc, file_name)}.html"):
            logger.info(f"successfully download {self.doi} from {publisher}, located at {os.path.join(self.download_loc, file_name)}.html")
        else:
            logger.info(f"sorry, {os.path.join(self.download_loc, file_name)}.html is empty, something went wrong")
        return None


def validation(abs_file_path):
    with open(abs_file_path, 'rb') as fi:
        line_list = fi.readlines()
        if len(line_list) == 0:
            return False
        return True

def curl(user_agent, url, abs_file_path):
    subprocess.run(["curl", "-L", "-H", f"User-Agent: {user_agent}", "-o", abs_file_path, url], check=True)

doi = "10.1002/slct.201902017"
root, _ = os.path.split(__file__)
loc = root + "/articles"
name = "1"
retrieve = Retrieve(doi, loc)
retrieve.download(name)
# TODO: the curl not works so well, maybe need to use the headless google chrome.