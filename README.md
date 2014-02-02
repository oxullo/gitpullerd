# gitpullerd

Gitpullerd is a handler for github post-push web hooks.

It keeps a local repo in sync with a remote branch and can execute local post-pull
scripts.

# Purpose

gitpullerd has been created to automate staging deployments of a web application.

# Dependencies

gitpullerd depends on the following python packages:

 * netaddr ( v0.7.7 https://pypi.python.org/pypi/netaddr/0.7.7 )
 * python-daemon ( v1.5.5 https://pypi.python.org/pypi/python-daemon/1.5.5 )
 * git ( v0.3.2 https://pypi.python.org/pypi/GitPython/0.3.2.RC1 )
 * lockfile ( v0.8 https://pypi.python.org/pypi/lockfile/0.8 )

__Note: python-daemon 1.5.5 is incompatible with lockfile 0.9.1__

Git-core must be installed for python git package to work properly.

# Configuration

A sample configuration can be found in _samples/config.ini_

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

# Service startup

A sample LSB-compliant SYSV script can be found in _samples/etc/init.d/gitpullerd_.

The script assumes that _/etc/default/gitpullerd_ is available and customised for the
needs. A sample of this file can be found in _samples/etc/default/gitpullerd_

# Notes

gitpullerd has been tested under Debian Wheezy (7.2).
