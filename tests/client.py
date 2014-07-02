#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests

def test(event, payload_file):
    payload = open(payload_file, 'r').read()
    headers = {'X-Github-Event': event}

    t = time.time()
    r = requests.post('http://localhost:8888', data={'payload': payload},
            headers=headers)

    print 'Event: %s HTTP reply: %d Time: %dms' % (event,
            r.status_code, (time.time() - t) * 1000)


if __name__ == '__main__':
    test('ping', 'ping_payload.json')
    test('push', 'push_payload.json')
