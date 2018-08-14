#!/usr/bin/env python3
# Extracts RPC API docs from bitcoin source files.

import sqlite3
import sys
import re
import json

if len(sys.argv) < 4:
    print("usage: load-docs.py <DB_FILE> <TAG> <FILE_PATH>")
    sys.exit(1)

dbfile, tag, filepath = sys.argv[1:4]

conn = sqlite3.connect(dbfile)
c = conn.cursor()

# Parse source code for RPC doc strings, using a state machine.
state = 'BEGIN'
name = None
msgs = []
startLine = -1
endLine = -1

def close():
    msg = "".join(msgs).replace(r"\n", "<br/>").replace(r"\"", "\"")
    deprecated = "DEPRECATED" in msg
    c.execute('''
        insert into docs (tag, func, message, deprecated, filepath, start_line, end_line)
        values (?, ?, ?, ?, ?, ?, ?)
    ''', [tag, name, msg, deprecated, filepath, startLine, endLine])

for lineNum, line in enumerate(map(str.rstrip, sys.stdin)):
    if state == 'BEGIN':
        m = re.match(r"^(?:static\s+)?\w+ (\w+)\(.*?\)$", line)
        if m:
            state = 'FUNC'
            name = m[1]
            msgs = []
            startLine = lineNum
    elif state == 'FUNC':
        m = re.match("^{", line)
        if m:
            state = 'BODY'
        else:
            state = 'BEGIN'
    elif state == 'BODY':
        m = re.match("^\s*?if \(.*(?:\w+equest\.)?fHelp.*?\)?(?:\s+\{)?$", line)
        if m:
            state = 'HELP'
        elif line == '}':
            state = 'BEGIN'
    elif state == 'HELP':
        m = re.match("\s*throw (?:std::)?runtime_error\($", line)
        s = re.match(r"^\s*(?:.*? = )?(\"(.*)\")?(\);)?$", line, re.DOTALL)
        if re.match("\s*\{", line):
            continue
        elif m:
            state = 'MSG'
        elif s:
            # This is a line like `string msg = "lorem ipsum"`. The `throw runtime_error` will come later.
            if s[2]:
                msgs.append(s[2])
                state = 'MSG'
            if s[3]:
                close()
                state = 'BEGIN'
        elif re.match("\s*\(.*", line):
            # Continuation of the fHelp conditional.
            continue
        else:
            state = 'BODY'
    elif state == 'MSG':
        m = re.match(r"^\s*(\"(.*)\")?(\);)?$", line, re.DOTALL)
        cx = re.match(r"\s*\+ HelpExampleCli\(\"(.*?)\", \"(.*)\"\)(?:\s+\+)?$", line)
        rx = re.match(r"\s*\+ HelpExampleRpc\(\"(.*?)\", \"(.*)\"\)(?:\s+\+)?$", line)
        if m:
            if m[2]:
                msgs.append(m[2])
            if m[3]:
                endLine = lineNum
                close()
                state = 'BEGIN'
        elif cx:
            # CLI Example.
            msgs.append(r"> bitcoin-cli {} {}\n".format(cx[1], cx[2]))
        elif rx:
            # RPC Example.
            msgs.append(r"> curl --user myusername --data-binary '{{\"jsonrpc\": \"1.0\", \"id\":\"curltest\", \"method\": \"{}\", \"params\": [{}] }}' -H 'content-type: text/plain;' http://127.0.0.1:8332/\n".format(rx[1], rx[2]))
        else:
            endLine = lineNum
            close()
            state = 'BEGIN'

conn.commit()
conn.close()
