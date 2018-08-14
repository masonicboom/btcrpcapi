#!/usr/bin/env python3
# Generates webpage charting RPC API calls for each Bitcoin version.

import sys
import os
import collections
import datetime
import json
import hashlib
import sqlite3

def header(relpath=""):
    return '''
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="{}style.css">
        </head>
        <body>
    '''.format(relpath)

def footer():
    return '''
    </body>
    </html>
    '''

def legend():
    return '''
    <div id="legend">
    <h3>Legend</h3>
    <table>
        <tr><td class="present"></td><td>Call Active</td></tr>
        <tr><td class="present deprecated"></td><td>Call Deprecated</td></tr>
        <tr><td class="present msg-changed"></td><td>Message Changed (Active)</td></tr>
        <tr><td class="present deprecated msg-changed"></td><td>Message Changed (Deprecated)</td></tr>
    </table>
    </div>
    '''

# If cat is specified, restricts chart output to only calls in that category.
def chart(dbcursor, cat=None, relpath=""):
    parts = []
    parts.append('''
    <table id="chart">
    <thead>
        <tr>
            <th>Call</th>
    ''')

    # Select list of tags that have any API docs, ascending by tag (version).
    sql = '''
        select tag
        from rels
        where tag in (
            select distinct tag
            from rels
            join apis using (tag)
        )
        order by major asc, minor asc, patch asc
    '''
    dbcursor.execute(sql)
    tags = [r[0] for r in dbcursor.fetchall()]
    for tag in tags:
        parts.append('<th><span class="version"><a href="{}tags/{}.html">{}</a></span></th>'.format(relpath, tag, tag))

    parts.append('<th>Call</th>')
    if cat == None:
        parts.append('<th>Category</th>')
    
    parts.append('''            
        </tr>
    </thead>
    <tbody>
    ''')

    # Select calls, sorted by earliest and latest versions they're present in. Chooses the category of the call in the last version as the category for that call (TODO: treat (call, category) pairs as distinct calls),
    sql = '''
        with vers as (
            select
                call,
                category,
                tag,
                printf("%03d.%03d.%03d", major, minor, patch) as ver
            from apis
            join rels using (tag)
        ), mins as (
            select
                call,
                min(ver) as min_ver
            from vers
            group by call
        ), maxs as (
            select
                call,
                max(ver) as max_ver
            from vers
            group by call
        ), min_tags as (
            select
                vers.call,
                vers.ver,
                tag
            from vers
            join mins on vers.call = mins.call and vers.ver = mins.min_ver
        ), max_tags as (
            select
                vers.call,
                vers.ver,
                vers.category,
                tag
            from vers
            join maxs on vers.call = maxs.call and vers.ver = maxs.max_ver
        )
        select
            min_tags.call,
            max_tags.category
        from min_tags
        join max_tags using (call)
        order by min_tags.ver asc, max_tags.ver asc, category asc, call asc
        ;
    '''
    dbcursor.execute(sql)
    callRows = dbcursor.fetchall()
    for [call, category] in callRows:
        msghash = None # Tracks differences in messages between versions.

        if cat != None and category != cat:
            continue

        parts.append('<tr>')
        parts.append('<td>{}</td>'.format(call))

        # Select docs data for each version of call.
        sql = '''
            select
                apis.tag,
                message,
                deprecated
            from docs
            join apis using (tag, func)
            join rels using (tag)
            where call = ?
            order by major asc, minor asc, patch asc
        '''
        callDocs = {} # Map from tag -> docs.
        for [tag, message, deprecated] in dbcursor.execute(sql, [call]):
            callDocs[tag] = [message, deprecated]

        for tag in tags:
            if tag not in callDocs:
                parts.append('<td title="{}"></td>'.format(tag))
                continue
            
            [message, deprecated] = callDocs[tag]

            p = "docs/{}/{}.html".format(tag, call)
            link = ""
            if os.path.exists(p):
                link = '<a href="{}{}">?</a>'.format(relpath, p)
            
            # Check if the message changed from the previous version. If so, vary the color.
            msgchanged = False

            newhash = hashlib.sha256(message.encode("utf-8")).hexdigest()
            if msghash != None and newhash != msghash:
                msgchanged = True
            msghash = newhash
        
            changedClass = ""
            if msgchanged:
                changedClass = "msg-changed"
            
            deprecatedClass = ""
            if deprecated:
                deprecatedClass = "deprecated"

            parts.append('<td title="{}" class="present {} {}">{}</td>'.format(tag, changedClass, deprecatedClass, link))

        parts.append('<td>{}</td>'.format(call))
        if cat == None:
            parts.append('<td><a href="cats/{}.html">{}</a></td>'.format(category, category))
        parts.append('</tr>')

    parts.append('''
        </tbody>
    </table>
    ''')

    return '\n'.join(parts)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: generate-docs.py <DB_FILE>")
        sys.exit(1)

    dbfile = sys.argv[1]

    # Open DB.
    conn = sqlite3.connect(dbfile)
    dbcursor = conn.cursor()

    # Dump output as HTML.
    print(header())

    print('''
        <h1>A Map of the Bitcoin Core RPC API across Versions</h1>
        <h3>By <a href="https://masonsimon.com">Mason Simon</a></h3>
    ''')

    print('<h3>Last updated {}.</h3>'.format(datetime.date.today()))

    print(legend())

    print(chart(dbcursor))

    print(footer())

    conn.close()