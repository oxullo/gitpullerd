#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

import git

import server
import config

logger = logging.getLogger(__name__)


class App(object):
    def __init__(self, ):
        try:
            self.__repo = git.Repo(cfg['target_path'])
        except git.exc.NoSuchPathError:
            logger.warning('Target path not a git repo, cloning')
            self.__repo = git.Repo.clone_from(cfg['source_url'], cfg['target_path'])

        self.__repo.git.checkout(cfg['target_branch'])

        self.__server = server.create_server(cfg['webhook_listen_ip'],
                int(cfg['webhook_listen_port']))
        server.set_payload_handler(self.__payload_handler)

    def run(self):
        try:
            self.__server.serve_forever()
        except KeyboardInterrupt:
            logger.info('Terminating')

    def __payload_handler(self, payload):
        print 'PAYLOAD:', payload
        self.__repo.git.pull()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cfg = config.Config()
    cfg.from_file('../tests/config.ini')
    app = App()
    app.run()
