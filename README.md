# gitpullerd

Gitpullerd is a handler for github post-push web hooks.

It keeps a local repo in sync with a remote branch and can execute local post-pull
scripts.

# Purpose

gitpullerd has been created to automate staging deployments of a web application.

# Dependencies

gitpullerd depends on the following python packages:

 * setuptools
 * netaddr ( v0.7.7 https://pypi.python.org/pypi/netaddr/0.7.7 )
 * python-daemon ( v1.5.5 https://pypi.python.org/pypi/python-daemon/1.5.5 )
 * git ( v0.3.2 https://pypi.python.org/pypi/GitPython/0.3.2.RC1 )
 * lockfile ( v0.8 https://pypi.python.org/pypi/lockfile/0.8 )
 * voluptuous ( v0.8.4 https://pypi.python.org/pypi/voluptuous/ )

__Note: python-daemon 1.5.5 is incompatible with lockfile 0.9.1__

Git-core must be installed for python git package to work properly.

# Installation

    # git clone https://github.com/oxullo/gitpullerd
    # python setup.py build && python setup.py install
    # cp samples/etc/init.d/gitpullerd /etc/init.d/
    # mkdir /etc/gitpullerd /var/log/gitpullerd /var/run/gitpullerd
    # chown <user>:<group> /var/log/gitpullerd /var/run/gitpullerd
    # cp samples/gitpullerd.ini.sample /etc/gitpullerd/gitpullerd.ini

Edit /etc/gitpullerd/config.ini

A debian-style default config file is added too and can be used instead of altering the init.d file:

    # cp samples/etc/default/gitpullerd /etc/default/

Automate the startup with:x

    # update-rc.d gitpullerd defaults

# Configuration

A sample configuration can be found in _samples/gitpullerd.ini.sample_

Explanation of the config fields:

 * _source/url_: the URL gitpullerd should clone from (git and http/s schemes supported)
 * _target/path_: path of the local repository copy. It must be writeable by the user that
 launches gitpulld
 * _target/branch_: gitpullerd performs a checkout of this branch before pulling
 * _webhook/listen_ip_: listen IP, 0.0.0.0 to listen to all interfaces
 * _webhook/listen_port_: listen port
 * _webhook/allowed_networks_: comma separated list of networks allowed to trigger operations
 * _payload/match_url_: the repository "url" field specified in the hook payload must
 match this field in order to trigger the pull
 * _payload/match_ref_: the "ref" field of the payload must match this field in order to
 trigger the pull
 * _action/shell_: shell script to be executed upon successful pull

It might be handy to test the configuration by using the _-f_ option while invoking
gitpullerd for the first time.

# Github webhook

Add a webhook that points to the public address of the server where gitpullerd runs,
use the port specified in the configuration file:

    Payload URL: http://public.address:8888
    Content-type: application/json

# Testing

A test script can be found in tests/client.py. It requires the python package requests.

# Notes

gitpullerd has been tested under Debian Wheezy (7.2).
