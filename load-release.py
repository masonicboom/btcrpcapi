#!/usr/bin/env python3
# Loads metadata about a release into the database.

import sqlite3
import sys
import re

if len(sys.argv) < 4:
    print("usage: load-release.py <DB_FILE> <TAG> <GIT_COMMIT_HASH>")
    sys.exit(1)

dbfile, tag, githash = sys.argv[1:4]

# Extract major.minor.patch from tag.
m = re.match(r'v(\d+)\.(\d+)\.(\d+)', tag)
if tag == 'master':
    # HACK: this causes "master" to sort after all the other tags.
    major, minor, patch = 9999, 9999, 9999
elif m:
    major, minor, patch = m[1], m[2], m[3]
else:
    sys.exit('Unrecognized tag format: {}'.format(tag))

# Load into database.
conn = sqlite3.connect(dbfile)
c = conn.cursor()
c.execute('''
    insert into rels (tag, major, minor, patch, githash)
    values (?, ?, ?, ?, ?)
''', [tag, major, minor, patch, githash])
conn.commit()
conn.close()
