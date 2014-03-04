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

import subprocess
import select
import logging

logger = logging.getLogger(__name__)


class Spawner(object):
    def __init__(self, command, args=[]):
        self.__command = [command]
        self.__command += args

    def execute(self):
        proc = subprocess.Popen(self.__command, shell=True, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

        out_fd = proc.stdout.fileno()
        err_fd = proc.stderr.fileno()

        while True:
            rlist, _, _ = select.select([out_fd, err_fd], [], [])

            if proc.poll() != None:
                break

            for fd in rlist:
                if fd == out_fd:
                    logger.info('OUT: %s' % proc.stdout.readline().strip())
                elif fd == err_fd:
                    logger.info('ERR: %s' % proc.stderr.readline().strip())

        return proc.returncode
