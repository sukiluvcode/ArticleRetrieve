"""
retrieve articles from elsevier, wiley, springer nature, science, rsc, not include acs specifically.
wiley and aaas for some reason are yet not supported. (breifly saying, can render in browser, however failed in python)
"""
import os
import re
import time
import logging
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

        if publisher == ("acs" or "aaas"):
            logger.info(
                f"sorry, scrawler is forbidden in {publisher}")
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
            downloader = ArticleDownloader()
            my_file = open(f"{self.download_loc}/{file_name}.xml", 'wb')
            downloader.get_xml_from_doi(
                doi=self.doi, writefile=my_file, mode=publisher)
            my_file.close()
            if validation(f"{os.path.join(self.download_loc, file_name)}.xml"):
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

# doi = "10.1016/j.mtcomm.2022.104823"
# root, _ = os.path.split(__file__)
# loc = root + "/articles"
# name = "1"
# retrieve = Retrieve(doi, loc)
# retrieve.download(name)