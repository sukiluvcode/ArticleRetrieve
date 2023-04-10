"""
module from olivettigroup.
The url of repository was "https://github.com/olivettigroup/article-downloader"
i. In get_html_from_doi function, Wiley section, change the url to 
https://onlinelibrary.wiley.com/doi/full-xml/{doi}
ii. replace the "@trace" with "@log_decorator"

"""

import requests


class ArticleDownloader:
    def __init__(self, els_api_key=None, springer_api_key=None, sleep_sec=1, timeout_sec=30):
        '''
        Initialize and set up API keys

        :param els_api_key: API key for Elsevier (for Elsevier's API)
        :type els_api_key: str
        :param sleep_sec: Sleep time between API calls (default = 1s)
        :type sleep_sec: int
        :param timeout_sec: Max time before timeout (default = 30s)
        :type timeout_sec: int
        '''
        self.els_api_key = els_api_key
        self.springer_api_key = springer_api_key
        self.sleep_sec = sleep_sec
        self.timeout_sec = timeout_sec

    def get_metadata_from_doi(self, doi, mailto="null@null.com"):
        base_url = 'https://api.crossref.org/works/' + str(doi)

        headers = {
            'Accept': 'application/json',
            'User-agent': 'mailto:' + mailto
        }

        search_url = str(base_url)
        response = requests.get(
            search_url, headers=headers, timeout=self.timeout_sec).json()

        item = response["message"]
        metadata_record = None
        try:
            if "volume" in item:
                volume = item["volume"]
            else:
                volume = None

            if "published-print" in item:
                year = item['published-print']['date-parts'][0][0]
            else:
                year = None

            if "issue" in item:
                issue = item["issue"]
            else:
                issue = None

            if "page" in item:
                page = item["page"]
            else:
                page = None

            metadata_record = {
                "doi": item["DOI"],
                "issn": item["ISSN"][0],
                "title": item["title"][0],
                "prefix": item["prefix"],
                "journal": item["container-title"][0],
                "publisher": item["publisher"],
                "volume": volume,
                "issue": issue,
                "page": page,
                "year": year,
                "num_references": item['references-count'],
                "times_cited": item['is-referenced-by-count']
            }
        except:
            pass

        return metadata_record

    def get_xml_from_doi(self, doi, writefile, mode):
        '''
        Downloads and writes an HTML article to a file, given a DOI and operating mode

        :param doi: DOI string for the article we want to download
        :type doi: str

        :param writefile: file object to write to
        :type writefile: file

        :param mode: choose from {'elsevier' | 'aps'}, depending on how we wish to access the file
        :type mode: str

        :returns: True on successful write, False otherwise
        :rtype: bool
        '''

        if mode == 'elsevier':
            try:
                xml_url = 'https://api.elsevier.com/content/article/doi/' + doi + '?view=FULL'
                headers = {
                    'X-ELS-APIKEY': self.els_api_key,
                    'Accept': 'text/xml'
                }

                r = requests.get(xml_url, stream=True,
                                 headers=headers, timeout=self.timeout_sec)
                if r.status_code == 200:
                    for chunk in r.iter_content(2048):
                        writefile.write(chunk)
                    return True
            except:
                # API download limit exceeded
                return False
            return False

        if mode == 'wiley':
            base_url = 'https://onlinelibrary.wiley.com/doi/' #  https://onlinelibrary.wiley.com/doi/full-xml/10.1002/slct.201902017
            api_url = base_url + "full-xml/" + doi

        try:
            headers = {
                'Accept': 'text/xml',
                'User-agent': 'Mozilla/5.0'
            }
            r = requests.get(api_url, stream=True,
                                headers=headers, timeout=self.timeout_sec)
            if r.status_code == 200:
                for chunk in r.iter_content(2048):
                    writefile.write(chunk)
                return True
        except:
            return False
        return False

        if mode == 'aps':
            try:
                xml_url = 'http://harvest.aps.org/v2/journals/articles/' + doi
                headers = {
                    'Accept': 'text/xml'
                }

                r = requests.get(xml_url, stream=True,
                                 headers=headers, timeout=self.timeout_sec)
                if r.status_code == 200:
                    for chunk in r.iter_content(2048):
                        writefile.write(chunk)
                    return True
            except:
                # API download limit exceeded
                return False
            return False

        return False

    def get_html_from_doi(self, doi, writefile, mode):
        '''
        Downloads and writes an HTML article to a file, given a DOI and operating mode

        :param doi: DOI string for the article we want to download
        :type doi: str

        :param writefile: file object to write to
        :type writefile: file

        :param mode: choose from {'elsevier' | 'springer' | 'acs' | 'ecs' | 'rsc' | 'nature' | 'wiley' | 'aaas' | 'emerald'}, depending on how we wish to access the file
        :type mode: str

        :returns: True on successful write, False otherwise
        :rtype: bool
        '''

        if mode == 'springer':
            base_url = 'https://www.nature.com/articles/'
            prefix, bulk = doi.split('/')
            api_url = base_url + bulk

            try:
                headers = {
                    'Accept': 'text/html',
                    'User-agent': 'Mozilla/5.0',
                    'api_key': self.springer_api_key
                }
                r = requests.get(api_url, stream=True,
                                 headers=headers, timeout=self.timeout_sec)
                if r.status_code == 200:
                    for chunk in r.iter_content(2048):
                        writefile.write(chunk)
                    return True
            except:
                return False
            return False

        if mode == 'acs':
            base_url = 'http://pubs.acs.org/doi/full/' 
            api_url = base_url + doi

            try:
                headers = {
                    'Accept': 'text/html',
                    'User-agent': 'Mozilla/5.0'
                }
                r = requests.get(api_url, stream=True,
                                 headers=headers, timeout=self.timeout_sec)
                if r.status_code == 200:
                    for chunk in r.iter_content(2048):
                        writefile.write(chunk)
                    return True
            except:
                return False
            return False

        if mode == 'emerald':
            base_url = 'http://www.emeraldinsight.com/doi/full/'
            api_url = base_url + doi

            try:
                headers = {
                    'Accept': 'text/html',
                    'User-agent': 'Mozilla/5.0'
                }
                r = requests.get(api_url, stream=True,
                                 headers=headers, timeout=self.timeout_sec)
                if r.status_code == 200:
                    for chunk in r.iter_content(2048):
                        writefile.write(chunk)
                    return True
            except:
                return False
            return False

        if mode == 'rsc':
            html_string = 'articlehtml'
            download_url = 'https://doi.org/' + doi
            headers = {
                'Accept': 'text/html',
                'User-agent': 'Mozilla/5.0'
            }
            r = requests.get(download_url, headers=headers,
                             timeout=self.timeout_sec)
            url = r.url
            url = url.encode('ascii')
            url = url.decode()
            url = url.split('/')
            url = url[0] + '//' + url[2] + '/' + url[3] + '/' + url[4] + \
                '/' + html_string + '/' + url[6] + '/' + url[7] + '/' + url[8]

            r = requests.get(url, stream=True, headers=headers,
                             timeout=self.timeout_sec)

            if r.status_code == 200:
                try:
                    for chunk in r.iter_content(2048):
                        writefile.write(chunk)
                    return True
                except:
                    return False

            return False

        if mode == 'nature':
            download_url = 'https://www.nature.com/articles/' + doi

            headers = {
                'Accept': 'text/html',
                'User-agent': 'Mozilla/5.0'
            }
            r = requests.get(download_url, stream=True,
                             headers=headers, timeout=self.timeout_sec)
            if r.status_code == 200:
                try:
                    for chunk in r.iter_content(2048):
                        writefile.write(chunk)
                    return True
                except:
                    return False
            return False

        if mode == 'aaas':

            headers = {
                'Accept': 'text/html',
                'User-agent': 'Mozilla/5.0'
            }

            article_url = 'https://doi.org/' + doi
            resp = requests.get(article_url, headers=headers,
                                timeout=self.timeout_sec)

            download_url = resp.url + '.full'  # Capture fulltext from redirect

            r = requests.get(download_url, stream=True,
                             headers=headers, timeout=self.timeout_sec)
            if r.status_code == 200:
                try:
                    for chunk in r.iter_content(2048):
                        writefile.write(chunk)
                    return True
                except:
                    return False
            return False

        if mode == 'ecs':
            headers = {
                'Accept': 'text/html',
                'User-agent': 'Mozilla/5.0'
            }

            article_url = 'https://doi.org/' + doi
            resp = requests.get(article_url, headers=headers,
                                timeout=self.timeout_sec)

            download_url = resp.url + '.full'  # Capture fulltext from redirect

            r = requests.get(download_url, stream=True,
                             headers=headers, timeout=self.timeout_sec)
            if r.status_code == 200:
                try:
                    for chunk in r.iter_content(2048):
                        writefile.write(chunk)
                    return True
                except:
                    return False
            return False

        return False
