#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2017 OXullo Intersecans (x@brainrapers.org)
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

import sys
import os
import time
import logging
import shutil
import Queue
import atexit

import git

import server
import config

import gitpullerd
import spawner
import payload_tester

logger = logging.getLogger(__name__)


class App(object):
    def __init__(self, cfg):
        logger.info('gitpullerd v%s starting up' % gitpullerd.__version__)
        atexit.register(lambda: logger.info('shutting down'))

        self.__cfg = cfg
        self.__payload_queue = Queue.Queue()
        self.__payload_tester = payload_tester.PayloadTester(
                self.__cfg['payload_match_url'],
                self.__cfg['payload_match_ref'],
                self.__cfg['target_branch'])

        self.__init_git()
        if not self.__repo.bare:
            self.__checkout()
            self.__pull()
        else:
            self.__fetch()

        self.__init_server()

    def run(self):
        self.__server.serve_forever_async()
        while True:
            try:
                # Timeout works around the impossibility to interrupt Queue.get()
                # with ctrl-c: http://bugs.python.org/issue1360
                payload = self.__payload_queue.get(True, 1)
                self.__process_payload(payload)
            except KeyboardInterrupt:
                self.__server.shutdown()
                sys.exit(0)
            except Queue.Empty:
                pass
            except Exception, e:
                logger.error('Caught an exception while iterating loop:')
                logger.exception(e, exc_info=sys.exc_info)
                time.sleep(1)

    def __init_git(self):
        logger.info('Initializing target path: %s' % self.__cfg['target_path'])
        try:
            self.__repo = git.Repo(self.__cfg['target_path'])
            logger.info('Valid git repository found (bare=%s)' % self.__repo.bare)
        except (git.exc.NoSuchPathError, git.exc.InvalidGitRepositoryError):
            if os.path.exists(self.__cfg['target_path']):
                shutil.rmtree(self.__cfg['target_path'])

            logger.warning('Target path not a git repo or invalid, cloning')
            self.__repo = git.Repo.clone_from(self.__cfg['source_url'],
                    self.__cfg['target_path'])

    def __checkout(self):
        self.__repo.git.checkout(self.__cfg['target_branch'])
        logger.info('Checked out branch: %s' % self.__repo.active_branch.name)

    def __pull(self):
        self.__repo.git.pull()
        logger.info('Pulled up to revision: %s' % self.__repo.active_branch.commit)

    def __fetch(self):
        self.__repo.git.fetch()
        logger.info('Fetched up to revision: %s' % self.__repo.active_branch.commit)

    def __init_server(self):
        self.__server = server.create_server(self.__cfg['webhook_listen_ip'],
                int(self.__cfg['webhook_listen_port']))
        server.set_payload_handler(self.__receive_payload)

        allowed_networks = self.__cfg['webhook_allowed_networks']
        if allowed_networks:
            ip_list = [ip.strip() for ip in allowed_networks.split(',')]
            server.set_allowed_networks(ip_list)
        else:
            logger.fatal('No webhook/allowed_networks defined')
            sys.exit(1)

    def __receive_payload(self, payload_data):
        self.__payload_queue.put(payload_data)

    def __process_payload(self, payload_data):
        if self.__payload_tester.process(payload_data):
            logger.info('Payload filters match, updating')
            try:
                if not self.__repo.bare:
                    self.__pull()
                else:
                    self.__fetch()
            except Exception, e:
                logger.error('Cannot update: %s' % str(e))
            else:
                logger.info('Update successful')
                self.__run_action()
        else:
            logger.info('Ignoring request')

    def __run_action(self):
        if self.__cfg['action_shell']:
            logger.info('Executing post-pull action: %s' % self.__cfg['action_shell'])

            spawner_obj = spawner.Spawner(self.__cfg['action_shell'])
            rc = spawner_obj.execute()

            if rc == 0:
                logger.info('Action terminated successfully')
            else:
                logger.error('Action terminated with return code %d' % rc)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    cfg = config.Config()
    cfg.from_file('../tests/config.ini')
    app = App(cfg)
    app.run()
