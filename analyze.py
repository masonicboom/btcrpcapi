#!/usr/bin/env python3
# Processes API call lists for each bitcoin version into dataset containing API call, earliest release it appeared in, and latest release it appeared in.

import sys
import os
import collections
import datetime

# Functions to transform 'vX.Y.Z' <=> [X, Y, Z] for sorting.
def version2list(v):
    if v == 'master':
        return [float('inf'), float('inf'), float('inf')]
    return [int(x) for x in v[1:].split('.')]

def list2version(vl):
    return 'v{}'.format('.'.join([str(v) for v in vl]))

# Map from call -> version -> present.
calls = collections.defaultdict(set)

# Map from call -> function name that implements that call.
funcs = collections.defaultdict(dict)

# Map from call -> first version it appeared in.
earliest = {}

# Map from call -> last version it appeared in.
latest = {}

# Very first version with any 
first = None

# Compute set of all versions.
versions = set()
for fn in os.listdir('apis/'):
    versions.add(fn)

# Compute calls in each version, and first and last version that each call appeared in.
for v in sorted(versions, key=lambda k: version2list(k)):
    vl = version2list(v)
    f = open('apis/{}'.format(v), 'r')
    for line in f.readlines():
        parts = line.rstrip().split()
        call, func = parts[0], parts[1]
        calls[call].add(v)
        funcs[call][v] = func

        if call not in earliest:
            earliest[call] = vl
        latest[call] = vl

# Very first version with any calls.
first = sorted(earliest.values())[0]

# Dump output as HTML.
print('''
<html>
<head>
    <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>

<h1>A Map of the Bitcoin Core RPC API across Versions</h1>
<h3>By <a href="https://masonsimon.com">Mason Simon</a></h3>
''')

print('<h3>Last updated {}.</h3>'.format(datetime.date.today()))

print('''
<table>
<thead>
    <tr>
        <th>Call</th>
''')

for v in sorted(versions, key=lambda k: version2list(k)):
    vl = version2list(v)
    if vl < first:
        continue
    print('<th><span class="version">{}</span></th>'.format(v))

print('''
        <th>Call</th>
    </tr>
</thead>
<tbody>
''')

for call in sorted(calls.keys(), key=lambda k: (earliest[k], latest[k], k)):
    print('<tr>')
    print('<td>{}</td>'.format(call))
    for v in sorted(versions, key=lambda k: version2list(k)):
        vl = version2list(v)
        if vl < first:
            continue
        if v in (calls[call]):
            p = "docs/{}/{}.html".format(v, funcs[call][v])
            link = ""
            if os.path.exists(p):
                link = '<a href="{}">?</a>'.format(p)
            print('<td title="{}" class="present">{}</td>'.format(v, link))
        else:
            print('<td title="{}"></td>'.format(v))
    print('<td>{}</td>'.format(call))
    print('</tr>')

print('''
    </tbody>
</table>
</body>
</html>
''')