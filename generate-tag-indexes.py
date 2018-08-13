#!/usr/bin/env python3
# Generates index page for all calls in a particular release tag.

import sys
import sqlite3
import subprocess

if len(sys.argv) < 2:
    print("usage: generate-tag-indexes.py <DB_FILE>")
    sys.exit(1)

dbfile = sys.argv[1]

conn = sqlite3.connect(dbfile)
dbcursor = conn.cursor()

def tag2html(tag):
    parts = []
    parts.append("""
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="../style.css">
    </head>
    <body>
    <h1>{}</h1>

    <table>
        <thead>
            <tr>
                <th>Category</th>
                <th>Call</th>
            </tr>
        </thead>
        <tbody>
    """.format(tag))

    sql = '''
        select
            category,
            call
        from apis
        where tag = ?
        order by category asc, call asc
    '''
    for [category, call] in dbcursor.execute(sql, [tag]):
        parts.append("<tr>")

        if category == None:
            link = '<i>N/A</i>'
        else:
            link = '<a href="../cats/{}.html">{}</a>'.format(category, category)
        parts.append('<td>{}</td>'.format(link))
        
        parts.append('<td><a href="../docs/{}/{}.html">{}</a></td>'.format(tag, call, call))

        parts.append('</tr>')

    parts.append("""
        </tbody>
    </table>
    </body>
    </html>
    """)

    return '\n'.join(parts).rstrip()


subprocess.run(['mkdir', '-p', 'tags'])

sql = '''
    select distinct tag
    from rels
    join apis using (tag)
'''
dbcursor.execute(sql)
tags = dbcursor.fetchall()
for [tag] in tags:
    html = tag2html(tag)
    with open('tags/{}.html'.format(tag), 'w') as f:
        f.write(html)

conn.close()
