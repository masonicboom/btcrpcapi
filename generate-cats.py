#!/usr/bin/env python3
# Generates an API doc chart for each category.

import sys
import sqlite3
import subprocess
import index
import datetime

if len(sys.argv) < 2:
    print("usage: generate-cat-indexes.py <DB_FILE>")
    sys.exit(1)

dbfile = sys.argv[1]

conn = sqlite3.connect(dbfile)
dbcursor = conn.cursor()

subprocess.run(['mkdir', '-p', 'cats'])

sql = '''
    select distinct category
    from apis
'''
dbcursor.execute(sql)
cats = dbcursor.fetchall()
for [cat] in cats:
    relpath = "../"
    
    with open('cats/{}.html'.format(cat), 'w') as f:
        f.write(index.header(relpath=relpath))

        f.write('<h1>{}</h1>'.format(cat))

        f.write('<h3>Last updated {}.</h3>'.format(datetime.date.today()))

        f.write(index.legend())

        f.write(index.chart(dbcursor, cat=cat, relpath=relpath))

        f.write(index.footer())

conn.close()
