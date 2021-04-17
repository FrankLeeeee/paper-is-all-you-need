#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file        : test_arxivlastestsubjectupdatecrawler
@description :
@time        : 2021/4/17 3:57 pm
@author      : Li Shenggui
@version     : 1.0
'''

from papercrawl.crawler import ArxivLatestSubjectUpdateCrawler


def test_arxiv_latest_subject_update_crawler():
    crawler = ArxivLatestSubjectUpdateCrawler(name='test',
                                              subject=['cs.Lg'],
                                              keywords=['transformer'],
                                              period=7)
    results = crawler.crawl()
    for paper in results:
        assert any(
            ['transformer' in paper.title.lower(),
             'transformer' in paper.abstract.lower()]), f'paper does not contain the keyword: {paper.title}'


if __name__ == '__main__':
    test_arxiv_latest_subject_update_crawler()
