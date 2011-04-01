#! /usr/bin/python

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker
from datetime import datetime, timedelta
import os

data = {}
for l in file("statfile.txt"):
    (ts, path, g, b, t) = l.strip().split(" ")
    ts = float(ts)
    g = int(g)
    b = int(b)
    t = int(t)
    if not data.has_key(path):
        data[path] = []
    data[path].append((datetime.fromtimestamp(ts), g+b, b, t+b+g))

for f in data.keys():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #cutoff = datetime.today() - timedelta(days=365)
    #data = filter(lambda x: x[0] > cutoff, data)
    (ts, g, b, t) = zip(*data[f])
    ax.plot(ts, t, 'k-')
    ax.plot(ts, g, 'g-')
    ax.plot(ts, b, 'r-')
    plt.fill_between(ts, b, 0, alpha=0.7, color="red")
    plt.fill_between(ts, g, b, alpha=0.7, color="green")
    plt.fill_between(ts, t, g, alpha=0.8, color="gray")
    fig.autofmt_xdate()
    if f == "TOTAL":
        fig.savefig("Html/total.png")
    else:
        outfile = "Html/%s.png" % (f,)
        try:
            os.makedirs(os.path.dirname(outfile))
        except OSError:
            pass

        fig.savefig(outfile)