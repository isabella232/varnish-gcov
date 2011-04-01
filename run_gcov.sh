#!/bin/sh

set -e

if [ `id -u` -eq 0 ] ; then
	echo "Don't run as root"
	exit 2
fi

cd $(dirname $0)
rm -rf Html/varnish-cache/* Html/*.png
#svn co http://varnish-cache.org/svn/trunk/varnish-cache || true
(
cd varnish-cache
git pull
if true ; then
	if true; then
		find . -name '*.gcov' -print | xargs rm -f
		find . -name '*.gcda' -print | xargs rm -f
		find . -name '*.gcno' -print | xargs rm -f

		make clean || true
		make distclean || true
		export CFLAGS="-fprofile-arcs -ftest-coverage -fstack-protector" 
		sh autogen.sh
		T=$(mktemp -d)
		./configure \
			--prefix=$T \
			--enable-debugging-symbols

		make 2>&1 | tee _.make
	fi

	if true ; then
		(
		# Get usage() run
		cd bin/varnishd
		./varnishd --help > /dev/null 2>&1 || true
		)
		make check | tee _.test
	fi

	find -name \*.o -execdir gcov {} \;
fi
)
find varnish-cache -name '*.gcov' -print | ./gcov_fmt.py >> statfile.txt
./plot.py
cd Html
git add .
git add --update .
git commit -m"Run $(date)"
