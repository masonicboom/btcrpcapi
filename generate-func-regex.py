#!/usr/bin/env python3
# Prints a regex to match definition lines for each RPC function in a release.

import sqlite3
import sys

if len(sys.argv) < 3:
    print("usage: load-release.py <DB_FILE> <TAG>")
    sys.exit(1)

dbfile, tag = sys.argv[1:3]

# Get list of function names.
conn = sqlite3.connect(dbfile)
c = conn.cursor()
c.execute('''
    select func from apis where tag = ?
''', [tag])
ret = c.fetchall()
conn.close()

# Print regex.
funcs = ['{}\('.format(f[0]) for f in ret]
print('|'.join(funcs))