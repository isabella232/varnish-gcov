#! /usr/bin/python

import os
from sys import argv
from datetime import datetime, timedelta
from os.path import join

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker

data = {}
for l in file(join(argv[1], "statfile.txt")):
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
        fig.savefig(join(argv[1], "total.png"))
    else:
        outfile = join(argv[1], "%s.png" % (f,))
        fig.savefig(outfile)
