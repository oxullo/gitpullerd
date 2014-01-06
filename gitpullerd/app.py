#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import logging
import Queue

import git

import server
import config

logger = logging.getLogger(__name__)


class App(object):
    def __init__(self, cfg):
        self.__cfg = cfg
        self.__payload_queue = Queue.Queue()

        self.__init_git()
        self.__repo.git.checkout(self.__cfg['target_branch'])

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
                logger.info('Terminating')
                self.__server.shutdown()
                sys.exit(0)
            except Queue.Empty:
                pass

    def __init_git(self):
        try:
            self.__repo = git.Repo(self.__cfg['target_path'])
        except git.exc.NoSuchPathError:
            logger.warning('Target path not a git repo, cloning')
            self.__repo = git.Repo.clone_from(self.__cfg['source_url'],
                    self.__cfg['target_path'])

    def __init_server(self):
        self.__server = server.create_server(self.__cfg['webhook_listen_ip'],
                int(self.__cfg['webhook_listen_port']))
        server.set_payload_handler(self.__receive_payload)

        whitelist = self.__cfg['webhook_allowed_ip_list']
        if whitelist:
            ip_list = [ip.strip() for ip in whitelist.split(',')]
            server.set_whitelist(ip_list)

    def __receive_payload(self, payload):
        self.__payload_queue.put(payload)

    def __process_payload(self, payload):
        logger.debug('Payload: %s' % payload)
        self.__repo.git.pull()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    cfg = config.Config()
    cfg.from_file('../tests/config.ini')
    app = App(cfg)
    app.run()
