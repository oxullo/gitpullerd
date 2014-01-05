#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import server

logger = logging.getLogger(__name__)


class App(object):
    def __init__(self):
        self.__server = server.create_server()
        server.set_payload_handler(self.__payload_handler)

    def run(self):
        self.__server.serve_forever()

    def __payload_handler(self, payload):
        print 'PAYLOAD:', payload


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = App()
    app.run()
