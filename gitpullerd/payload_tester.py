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

import logging
import urllib

import voluptuous


logger = logging.getLogger(__name__)


gh_payload_schema = voluptuous.Schema(
        {
        'repository': {'url': unicode},
        'ref': unicode,
        'commits': []},
        extra=True, required=True)

gh_commit_schema = voluptuous.Schema(
        {
        'id': unicode,
        'timestamp': unicode,
        'message': unicode,
        'committer': {'username': unicode},
        },
        extra=True, required=True)


class PayloadTester(object):
    def __init__(self, match_url, match_ref, target_branch):
        self.match_url = match_url
        self.match_ref = match_ref
        self.target_branch = target_branch

    def process(self, payload_data):
        logger.debug('Payload: %s' % payload_data)
        try:
            gh_payload_schema(payload_data)
        except voluptuous.Invalid, e:
            logger.error('Invalid payload: (error: %s)' % str(e))
            return False

        if (self.match_url
                and payload_data['repository']['url'].lower() != self.match_url.lower()):
            logger.warning('Payload url matching failed (wanted=%s got=%s)' %
                    (self.match_url, payload_data['repository']['url']))
            return False

        if self.match_ref == payload_data['ref']:
            logger.info('Pulling repo %s '
                    '(branch=%s)' % (payload_data['repository']['url'],
                    self.target_branch))

            for commit in payload_data['commits']:
                try:
                    gh_commit_schema(commit)
                except voluptuous.Invalid, e:
                    logger.warning('Invalid commit block, skipping info '
                            '(error: %s)' % str(e))
                else:
                    logger.info('  %s [%s..] (%s): %s' % (
                            commit['timestamp'],
                            commit['id'][:12],
                            commit['committer']['username'],
                            urllib.unquote_plus(commit['message'])))

            return True
