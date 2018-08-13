#!/usr/bin/env python3
# Creates a SQLite database to store doc data.

import sqlite3
import sys

if len(sys.argv) < 2:
    print("usage: init-db.py <DB_FILE>")
    sys.exit(1)

dbfile = sys.argv[1]

conn = sqlite3.connect(dbfile)
c = conn.cursor()

c.execute('''
    create table if not exists rels (
        tag text primary key,
        major number,
        minor number,
        patch number,
        githash text
    )
''')

c.execute('''
    create table if not exists apis (
        tag text,
        call text,
        func text,
        category text,
        foreign key(tag) references rels(tag)
    )
''')


c.execute('''
    create table if not exists docs (
        tag text,
        func text,
        message text,
        deprecated bool,
        filepath text,
        start_line number,
        end_line number,
        primary key (tag, func)
    )
''')

conn.commit()
conn.close()
