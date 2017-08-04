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
import logging
import argparse

import daemon
from daemon.pidlockfile import TimeoutPIDLockFile

import gitpullerd
import gitpullerd.config
import gitpullerd.app


def is_writable(file_name):
    if os.path.exists(file_name):
        return os.access(file_name, os.W_OK)
    else:
        return os.access(os.path.dirname(file_name), os.W_OK)

def fatal(message):
    print >>sys.stderr, 'ERROR: %s' % message
    sys.exit(1)

def parse_args():
    parser = argparse.ArgumentParser(description='git puller daemon')
    parser.add_argument('--config', '-c', metavar='CONFIGFILE', dest='config',
            default='/etc/gitpullerd/gitpullerd.ini', help='configuration file path')
    parser.add_argument('--pidfile', '-p', metavar='PIDFILE', dest='pidfile',
            default='/var/run/gitpullerd.pid', help='PID file path')
    parser.add_argument('--logfile', '-l', metavar='LOGFILE', dest='logfile',
            default=None, help='PID file path')
    parser.add_argument('--debug', '-d', dest='debug', action='store_true',
            help='run in debug mode')
    parser.add_argument('--foreground', '-f', dest='foreground', action='store_true',
            help='do not fork the process')

    return parser.parse_args()


def run():
    args = parse_args()

    if not os.path.isfile(args.config):
        fatal('Config file %s does not exist' % args.config)

    if not args.foreground and not is_writable(args.pidfile):
        fatal('Cannot write PID file %s' % args.pidfile)

    args.pidfile = os.path.abspath(args.pidfile)

    if args.logfile is not None and not is_writable(args.logfile):
        fatal('Cannot write to log file %s' % args.logfile)

    logger = logging.getLogger()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    if args.logfile is not None:
        handler = logging.FileHandler(args.logfile)
    else:
        handler = logging.StreamHandler(sys.stderr)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    cfg = gitpullerd.config.Config()
    cfg.from_file(args.config)

    if args.foreground:
        app = gitpullerd.app.App(cfg)
        app.run()
    else:
        daemon_context = daemon.DaemonContext(
                pidfile=TimeoutPIDLockFile(args.pidfile, 5),
                files_preserve=[handler.stream])

        with daemon_context:
            app = gitpullerd.app.App(cfg)

            try:
                app.run()
            except Exception, e:
                import traceback
                stack = traceback.format_exc()
                for line in stack.split('\n'):
                    logger.error(line)
