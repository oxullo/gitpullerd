#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser

class Config(dict):
    def __init__(self):
        super(Config, self).__init__()

    def from_file(self, file_name):
        conf = ConfigParser.ConfigParser()
        conf.read(file_name)
        for section in conf.sections():
            for option in conf.options(section):
                self.__setitem__('%s_%s' % (section, option), conf.get(section, option))


if __name__ == '__main__':
    c = Config()
    print c
    c.from_file('../tests/config.ini')
    print c
