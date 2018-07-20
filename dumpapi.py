#!/usr/bin/env python3
# Extracts RPC API calls from bitcoin source files.

import sys
import re

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
            if parts[0][0] == '"' and parts[1][0] == '"':
                print(parts[1].strip('"'))
            else:
                print(parts[0].strip('"'))