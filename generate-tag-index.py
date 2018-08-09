#!/usr/bin/env python3
# Generates index page for all calls in a particular release tag.

import sys

if len(sys.argv) < 2:
    print("usage: generate-tag-index.py <VERSION>")
    sys.exit(1)

version = sys.argv[1]

# List of {category, call, func} "structs" (dicts).
calls = []

# Older versions don't have categories. hascat tracks that.
hascat = False

with open("apis/{}".format(version)) as f:
    for line in f:
        parts = line.rstrip().split()
        if len(parts) == 2:
            calls.append({
                "call": parts[0],
                "func": parts[1]
            })
        elif len(parts) == 3:
            hascat = True
            calls.append({
                "call": parts[0],
                "func": parts[1],
                "cat": parts[2]
            })

print("""
<html>
<head>
    <link rel="stylesheet" type="text/css" href="../style.css">
</head>
<body>
<h1>{}</h1>

<table>
    <thead>
        <tr>
""".format(version))

if hascat:
    print("<th>Category</th>")

print("""
            <th>Call</th>
        </tr>
    </thead>
    <tbody>
""")

for c in sorted(calls, key=lambda k: [k.get("cat"), k.get("call")]):
    print("<tr>")

    if c.get("cat"):
        print('<td><a href="../cats/{}.html">{}</a></td>'.format(c["cat"], c["cat"]))
    

    func = c.get("func")
    if func == None:
        func = c["call"]
    
    print('<td><a href="../docs/{}/{}.html">{}'.format(version, func, c["call"]))

    print('</tr>')

print("""
    </tbody>
</table>
</body>
</html>
""")
