#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
