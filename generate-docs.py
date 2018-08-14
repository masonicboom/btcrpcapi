#!/usr/bin/env python3
# Generates a webpage for each RPC API call in each release.

import sys
import sqlite3
import subprocess

if len(sys.argv) < 2:
    print("usage: generate-docs.py <DB_FILE>")
    sys.exit(1)

dbfile = sys.argv[1]

def doc2html(name, category, version, message, githash, filepath, startLine, endLine):
    data = locals()
    return """
<html>
<head>
    <link rel="stylesheet" type="text/css" href="../../style.css">
</head>
<body>
<h1>{name}</h1>
<h2><a href="../../cats/{category}.html">{category}</a></h2>
<h2><a href="../../tags/{version}.html">{version}</a></h2>

<pre>
{message}
</pre>

<div class="source">
    Don't trust. Verify. Docs extracted from <a href="https://github.com/bitcoin/bitcoin/blob/{githash}/{filepath}#L{startLine}-L{endLine}">{filepath}#L{startLine}-L{endLine}</a>.
</div>
</body>
</html>
""".format(**data).lstrip()


conn = sqlite3.connect(dbfile)
c = conn.cursor()

sql = '''
    select
        call,
        category,
        rels.tag,
        message,
        githash,
        filepath,
        start_line,
        end_line
    from rels
    join apis on apis.tag = rels.tag
    join docs on docs.tag = apis.tag and docs.func = apis.func
'''
for row in c.execute(sql):
    tag = row[2]
    subprocess.run(['mkdir', '-p', 'docs/{}'.format(tag)])

    call = row[0]
    html = doc2html(*row)
    with open('docs/{}/{}.html'.format(tag, call), 'w') as f:
        f.write(html)

conn.close()
