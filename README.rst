Varnish Cache test coverage suite
=================================

Tools for measuring test suite coverage of Varnish Cache.

This code lives in git on https://github.com/varnish/varnish-gcov .


Prerequsites
------------

On Debian::

    # apt-get install lcov



Running
-------

Main script is "collect", which uses the git checkout in ``varnish-cache/``. It
will write to a tracefile given in the first argument::

    $ ./collect master.info
    [..]
    $ lcov --summary var/master.info
    Reading tracefile var/master.info
    lcov: WARNING: negative counts found in tracefile var/master.info
    Summary coverage rate:
      lines......: 82.4% (25245 of 30652 lines)
      functions..: 90.3% (1688 of 1870 functions)
      branches...: no data found


Authors
-------

Original author: Tollef Fog Heen.

Maintained by Lasse Karstensen <lkarsten@varnish-software.com>.


