#! /usr/bin/python

import sys, os
from time import time

prefix = "varnish-cache"

def main():
    when = time()
    s_good = s_bad = s_total = 0
    good = instrumented = 0
    fn = ""
    for f in sys.stdin:
        f = f.strip()
        if f.startswith("SF:"):
            fn = f.split(":",2)[1]
        elif f.startswith("LH:"):
            good = int(f.split(":",2)[1])
        elif f.startswith("LF:"):
            instrumented = int(f.split(":",2)[1])
        elif f == "end_of_record":
            if fn.find(prefix) >= 0:
                total = len(open(fn).readlines()) - instrumented
                bad = instrumented - good
                s_good += good
                s_bad += bad
                s_total += total
                print "%d varnish-cache%s %d %d %d" % (when,
                                                       fn.split(prefix,2)[1],
                                                       good, bad, total)
            good = instrumented = 0
            fn = ""
    print "%d TOTAL %d %d %d" % (when, s_good, s_bad, s_total)
    return 0

if __name__ == "__main__":
    sys.exit(main())
