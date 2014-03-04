#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2014 OXullo Intersecans (x@brainrapers.org)
#
# Foobar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar. If not, see <http://www.gnu.org/licenses/>.
#

import os
import ConfigParser

class InvalidConfig(Exception):
    pass


class Config(dict):
    def __init__(self):
        super(Config, self).__init__()

    def from_file(self, file_name):
        if not os.path.isfile(file_name):
            raise InvalidConfig('File %s not found' % file_name)

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
