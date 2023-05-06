#!/usr/bin/env python3

import sys

from fe.renderer.index import render_index

if len(sys.argv) != 3:
    print("generator must be called with two arguments year and target, e.g. index.py 2021 build/2020/index.html")
    sys.exit(1)

year = int(sys.argv[1])
target = sys.argv[2]
result = render_index(year)

with open(target, 'w') as f:
    f.write(result)
