#!/bin/bash -x
#
# apt-get install lcov

set -e

if [ `id -u` -eq 0 ] ; then
	echo "Don't run as root"
	exit 2
fi

cd $(dirname $0)
# rm -rf html/varnish-cache/* html/*.png varnish-cache
if [ ! -d "varnish-cache" ]; then
	git clone git://git.varnish-cache.org/varnish-cache
	cd varnish-cache
	export CFLAGS="-fprofile-arcs -ftest-coverage -fstack-protector"
	sh autogen.sh
	T=$(mktemp -d)
	./configure \
		--prefix=$T \
		--enable-debugging-symbols
	make 2>&1 | tee _.make
	cd ..
fi
cd varnish-cache

lcov --directory `pwd` --zerocounters
    (
    # Get usage() run
	cd bin/varnishd
	./varnishd --help > /dev/null 2>&1 || true
    )

make check | tee _.test
lcov --directory `pwd` --capture --output-file varnish.info
cd ..
echo "Done collecting. Formatting.."

./lcov_fmt.py < varnish-cache/varnish.info >> html/statfile.txt
genhtml --output-directory=html/varnish-cache varnish-cache/varnish.info
./plot.py html
#cd html

#git add .
#git add --update .
#git commit -m"Run $(date) Tree: $(cd ../varnish-cache && git describe --always)"
