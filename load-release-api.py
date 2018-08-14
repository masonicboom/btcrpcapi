#!/usr/bin/env python3
# Load RPC API calls from bitcoin source files into the database.

import sqlite3
import sys
import re

if len(sys.argv) < 3:
    print("usage: load-release-api.py <DB_FILE> <TAG>")
    sys.exit(1)

dbfile, tag = sys.argv[1:3]

# Extract APIs.
apis = []
in_rpcs = False
for line in map(str.rstrip, sys.stdin):
    if not in_rpcs:
        if re.match("static const CRPCCommand .*\[\] =", line):
            in_rpcs = True
    else:
        if line.startswith('};'):
            in_rpcs = False
        elif '{' in line and '"' in line:
            m = re.search('{(?: *([^,]+),)+', line)
            assert m, 'No match to table expression: %s' % line
            parts = [p.rstrip(',') for p in m.group(0).strip("{ },").split()]

            category = ""

            # The CRPC table format changed at some point. This handles that.
            if parts[0][0] == '"' and parts[1][0] == '"':
                # Column 0 is the category.
                category = parts[0].strip('"')
                col = 1
            else:
                col = 0

            # Output call and function name because docs will be indexed by function name.
            call_name = parts[col].strip('"')
            func_name = parts[col+1][1:]

            apis.append([tag, call_name, func_name, category])

# Load into database.
conn = sqlite3.connect(dbfile)
c = conn.cursor()
c.executemany('''
    insert into apis (tag, call, func, category)
    values (?, ?, ?, ?)
''', apis)
conn.commit()
conn.close()
