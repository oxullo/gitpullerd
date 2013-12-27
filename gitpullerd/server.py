#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urlparse
import logging
import BaseHTTPServer

logger = logging.getLogger(__name__)


class WebHookReqHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        logger.info(format % args)

    def do_POST(self):
        body = self.rfile.read(int(self.headers.getheader('content-length')))
        post_data = urlparse.parse_qs(body)

        if not 'payload' in post_data:
            logger.error('POST misses payload parameter')
            self.send_response(400)
            return

        payload_str = post_data['payload'][0]
        try:
            payload = json.loads(payload_str)
        except ValueError, e:
            logger.error('Cannot decode JSON payload string: %s' % payload_str)
            self.send_response(400)
            return

        self.send_response(200)

def create_server(address='0.0.0.0', port=8888):
    logger.info('Creating HTTPServer instance on %s:%d' % (address, port))
    return BaseHTTPServer.HTTPServer((address, port), WebHookReqHandler)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    server = create_server()
    server.serve_forever()
