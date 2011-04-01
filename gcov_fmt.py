#! /usr/bin/python

import sys, os
from time import time

def do_file(filename):
    l_good = l_bad = l_total = 0
    f = file(filename)
    outname = "Html/" + os.path.splitext(filename)[0] + ".html"
    try:
        os.makedirs(os.path.dirname(outname))
    except OSError:
        pass
    o = file(outname, "w")
    o.write("""<html><head><link rel="stylesheet" type="text/css" href="http://err.no/tmp/gcov.css" /></head><body>""")
    o.write("""<img src="%s.png" />\n""" % (os.path.basename(os.path.splitext(filename)[0]),))

    for l in f:
        (count, lineno, line) = l.strip().split(":", 2)
        c = "good"
        if count == "-":
            l_total += 1
            c = "ignored"
        elif count == "#####":
            l_bad += 1
            c = "bad"
        else:
            l_good += 1
        o.write("""<span class="code %s">%s</span>\n""" % (c, line))
    o.write("</body></html>")
    return (l_good, l_bad, l_total)

def main():
    when = time()
    good = bad = total = 0
    for f in sys.stdin:
        f = f.strip()
        (g,b,t) = do_file(f)
        good += g
        bad += b
        total += t
        print "%d %s %d %d %d" % (when, os.path.splitext(f)[0], g, b, t)
    print "%d TOTAL %d %d %d" % (when, good, bad, total)
    return 0

if __name__ == "__main__":
    sys.exit(main())
