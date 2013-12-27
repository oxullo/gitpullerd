#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

payload = open('sample_payload.json', 'r').read()

r = requests.post('http://localhost:8888', data={'payload': payload})
print r.status_code
