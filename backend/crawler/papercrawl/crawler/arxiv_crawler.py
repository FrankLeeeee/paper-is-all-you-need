#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file        : ArxivCrawler
@description :
@time        : 2021/4/17 2:20 pm
@author      : Li Shenggui
@version     : 1.0
'''

from datetime import date, datetime

import requests
from bs4 import BeautifulSoup as Soup

from papercrawl.data import Paper
from .base_crawler import BaseCrawler


class ArxivLatestSubjectUpdateCrawler(BaseCrawler):

    def __init__(self,
                 name: str,
                 subject: list,
                 keywords: list,
                 period: int,
                 ):
        super(ArxivLatestSubjectUpdateCrawler, self).__init__(name)
        self._subject = subject
        self._keywords = keywords
        self._base_url = 'http://export.arxiv.org/api/query?'
        self._period = period

    def _add_search_query(self, url: str):
        '''
        Add keywords and subjects to the search_query in the api.
        An example will be: http://export.arxiv.org/api/query?search_query=cat:cs.Lg+AND+ti:efficient

        reference to api parameters: https://arxiv.org/help/api/user-manual#Quickstart

        Args:
            url (str): the url to call to Arxiv

        Returns:
            url (str): the url to call to Arxiv
        '''

        def _convert_keyword_to_query(keyword: str):
            tokens = keyword.split()
            title_query = '+AND+'.join([f'ti:{t}' for t in tokens])
            abstract_query = '+AND+'.join([f'abs:{t}' for t in tokens])
            return f"%28{title_query}%29+OR+%28{abstract_query}%29"

        subject_query = [f'cat:{cat}' for cat in self._subject]
        subject_query = f"%28{'+OR+'.join(subject_query)}%29"

        keyword_query = [_convert_keyword_to_query(kw) for kw in self._keywords]
        keyword_query = f"%28{'+OR+'.join(keyword_query)}%29"

        result_url = f'{url}search_query={subject_query}+AND+{keyword_query}'
        return result_url

    def _add_sorting(self, url: str) -> str:
        '''
        add sorting parameters to the query url

        Args:
            url (str): the url to call to Arxiv

        Returns:
            url (str): the url to call to Arxiv

        '''
        result_url = f'{url}&sortBy=submittedDate&sortOrder=descending'
        return result_url

    def _add_range(self, url: str, start: int, max_result: int):
        '''
        add result range to the query url

        Args:
            url (str): the url to call to Arxiv

        Returns:
            url (str): the url to call to Arxiv

        '''
        result_url = f'{url}&start={start}&max_results={max_result}'
        return result_url

    def _within_period(self, today, published_date):
        delta = today - published_date
        if delta.days > self._period:
            return False
        else:
            return True

    def crawl(self) -> list:
        '''
        Crawl the latest paper from arxiv based on subject and keywords within the last
        <period> days.

        Returns:
            results (list): list of Paper objects

        '''

        # build query api
        query_api = self._add_search_query(self._base_url)
        query_api = self._add_sorting(query_api)

        # get today for checking period
        today = date.today()

        # crawl paper
        start_index = 0
        max_result_per_query = 20

        results = []
        out_of_period = False

        while True:
            temp_query_api = self._add_range(query_api, start_index, max_result_per_query)
            response = requests.get(temp_query_api)
            soup = Soup(response.content, 'lxml')

            all_entries = soup.find_all('entry')

            if len(all_entries) == 0:
                break

            for entry in all_entries:
                # check publish date
                published_date = entry.published.text
                published_date = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%SZ").date()
                if not self._within_period(today, published_date):
                    out_of_period = True
                    break

                # get paper info
                paper_url = entry.id.text
                title = entry.title.text.replace('\n ', '')
                abstract = entry.summary.text.replace('\n', '').strip()

                # check while keywords exist
                # this is because arxiv may use similar words to match the keywords
                # e.g. the word transformation will be matched with the keyword transformer
                title_match = [kw.lower() in title.lower() for kw in self._keywords]
                abstract_match = [kw.lower() in abstract.lower() for kw in self._keywords]

                if not any(title_match + abstract_match):
                    # if no exact keywords matching, skip
                    continue

                # get author info
                author_tags = entry.find_all('name')
                affiliation_tags = entry.find_all('arxiv:affiliation')

                author = [tag.text for tag in author_tags]
                affiliation = [tag.text for tag in affiliation_tags]

                paper = Paper(title=title,
                              author=author,
                              affiliation=affiliation,
                              abstract=abstract,
                              url=paper_url
                              )
                results.append(paper)

            if out_of_period:
                break

            start_index += max_result_per_query

        return results
