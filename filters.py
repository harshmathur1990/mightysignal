# -*- coding: utf-8 -*-


import copy

from dateutil import parser


class Filter(object):

    def __init__(self, field, op, value):
        self._field = field
        self._op = op
        self._value = value

    def filter(self, data):
        _rv = list()
        for _d in data:
            if self._op(_d.get(self._field), self._value):
                _rv.append(_d)
        return _rv


class CaseInsensitiveStringFilter(Filter):

    def filter(self, data):
        _rv = list()
        for _d in data:
            if self._op(_d.get(self._field).lower(), self._value.lower()):
                _rv.append(_d)
        return _rv


class DateFilter(Filter):

    def filter(self, data):
        _rv = list()
        for _d in data:
            if self._op(parser.parse(_d.get(self._field)).date(), self._value):
                _rv.append(_d)
        return _rv


class IntegerFilter(Filter):

    def filter(self, data):
        _rv = list()
        for _d in data:
            if self._op(int(_d.get(self._field)), self._value):
                _rv.append(_d)
        return _rv


class FilterChain(object):

    def __init__(self):
        self._filters = list()

    def add_filter(self, filter):
        self._filters.append(filter)
        return self

    def filter(self, results):
        if not results:
            return list()
        _rv = copy.deepcopy(results)
        for _filter in self._filters:
            _rv = _filter.filter(_rv)
        return _rv
