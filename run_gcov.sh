#!/bin/sh

set -e

if [ `id -u` -eq 0 ] ; then
	echo "Don't run as root"
	exit 2
fi

cd $(dirname $0)
rm -rf Html/varnish-cache/* Html/*.png varnish-cache
git clone git://git.varnish-cache.org/varnish-cache
(
    cd varnish-cache
    export CFLAGS="-fprofile-arcs -ftest-coverage -fstack-protector"
    sh autogen.sh
    T=$(mktemp -d)
    ./configure \
	--prefix=$T \
	--enable-debugging-symbols
    make 2>&1 | tee _.make
    lcov --directory `pwd` --zerocounters
    (
    # Get usage() run
	cd bin/varnishd
	./varnishd --help > /dev/null 2>&1 || true
    )
    make check | tee _.test
    lcov --directory `pwd` --capture --output-file varnish.info
)
./lcov_fmt.py < varnish-cache/varnish.info >> Html/statfile.txt
genhtml --output-directory=Html/varnish-cache varnish-cache/varnish.info
./plot.py
cd Html
git add .
git add --update .
git commit -m"Run $(date) Tree: $(cd ../varnish-cache && git describe --always)"
