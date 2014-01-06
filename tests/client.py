#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests

payload = open('sample_payload.json', 'r').read()

t = time.time()
r = requests.post('http://localhost:8888', data={'payload': payload})
print 'HTTP reply: %d Time: %dms' % (r.status_code, (time.time() - t) * 1000)
