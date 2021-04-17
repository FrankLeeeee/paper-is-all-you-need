#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file        : base_crawler
@description :
@time        : 2021/4/17 2:08 pm
@author      : Li Shenggui
@version     : 1.0
'''

from abc import ABC, abstractmethod


class BaseCrawler(ABC):

    def __init__(self,
                 name: str
                 ):
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def crawl(self, *args, **kwargs):
        pass
