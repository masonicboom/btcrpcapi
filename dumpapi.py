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

            # The CRPC table format changed at some point. This handles that.
            if parts[0][0] == '"' and parts[1][0] == '"':
                col = 1
            else:
                col = 0

            # Output call and function name because docs will be indexed by function name.
            call_name = parts[col].strip('"')
            func_name = parts[col+1][1:]
            print("{}\t{}".format(call_name, func_name))