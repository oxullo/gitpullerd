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

import json
import urlparse
import logging
import thread
import BaseHTTPServer

import netaddr

logger = logging.getLogger(__name__)


class WebHookReqHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    payload_handler = lambda v: None
    allowed_networks = []

    def log_message(self, format, *args):
        logger.info(format % args)

    def do_POST(self):
        logger.info('Processing POST request from %s' % str(self.client_address))

        source_ip = netaddr.IPAddress(self.client_address[0])
        if not any([source_ip in network for network in self.allowed_networks]):
            logger.warning('Access denied to client address %s' %
                    str(self.client_address))
            self.send_response(403)
            return

        body = self.rfile.read(int(self.headers.getheader('content-length')))
        event = self.headers.getheader('X-Github-Event')

        if event == 'ping':
            logger.info('Replying to ping')
            self.send_response(200)
            return
        elif event != 'push':
            logger.info('Invalid event: %s' % event)
            self.send_response(500)
            return

        if self.headers.getheader('content-type') == 'application/json':
            payload_str = body
        else:
            post_data = urlparse.parse_qs(body)
            if not 'payload' in post_data:
                logger.error('No payload available in the POST data')
                self.send_response(400)
                return

            payload_str = post_data['payload'][0]

        try:
            payload = json.loads(payload_str)
        except ValueError, e:
            logger.error('Cannot decode JSON payload string: %s' % payload_str)
            self.send_response(400)
            return

        try:
            self.payload_handler(payload)
        except Exception, e:
            logger.error('Error while calling payload handler: %s' % str(e))
            self.send_response(500)
        else:
            self.send_response(200)


class AsyncHTTPServer(BaseHTTPServer.HTTPServer):
    def serve_forever_async(self):
        thread.start_new_thread(self.serve_forever, ())


def create_server(address='0.0.0.0', port=8888):
    logger.info('Creating HTTPServer instance on %s:%d' % (address, port))
    return AsyncHTTPServer((address, port), WebHookReqHandler)

def set_payload_handler(handler):
    WebHookReqHandler.payload_handler = handler

def set_allowed_networks(ip_list):
    WebHookReqHandler.allowed_networks = [netaddr.IPNetwork(ip) for ip in ip_list]
    logger.info('Allowing access to networks: %s' % WebHookReqHandler.allowed_networks)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    server = create_server()
    server.serve_forever()
