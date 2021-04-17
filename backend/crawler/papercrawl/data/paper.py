#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file        : paper
@description :
@time        : 2021/4/17 3:31 pm
@author      : Li Shenggui
@version     : 1.0
'''


class Paper(object):

    def __init__(self,
                 title: str,
                 author: list,
                 affiliation: list,
                 abstract: str,
                 url: str
                 ):
        self._title = title
        self._author = author
        self._affiliation = affiliation
        self._abstract = abstract
        self._url = url

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._title

    @property
    def affiliation(self):
        return self._affiliation

    @property
    def abstract(self):
        return self._abstract

    @property
    def url(self):
        return self._url
