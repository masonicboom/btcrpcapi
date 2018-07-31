#!/usr/bin/env python3
# Extracts RPC API docs from bitcoin source files.

import sys
import re

if len(sys.argv) < 3:
    print("usage: dumpdocs.py <DOC_DIR> <VERSION>")
    sys.exit(1)

doc_dir = sys.argv[1]
version = sys.argv[2]

# Parse source code for RPC doc strings, using a state machine.
state = 'BEGIN'
name = None
msgs = []

def close():
    f = open("{}/{}/{}.html".format(doc_dir, version, name), "w")
    msg = "".join(msgs).replace(r"\n", "<br/>").replace(r"\"", "\"")
    html = """
    <html>
    <head>
    <style>
        body {{
            font-family: monospace;
            background-color: black;
            color: green;
        }}
    </style>
    </head>
    <body>
    <h1>{}</h1>
    <h2>{}</h2>
    {}
    </body>
    </html>
""".format(name, version, msg)
    f.write(html)
    f.close()

for line in map(str.rstrip, sys.stdin):
    if state == 'BEGIN':
        m = re.match("^\w+ (\w+)\(.*?\)$", line)
        if m:
            state = 'FUNC'
            name = m[1]
            msgs = []
    elif state == 'FUNC':
        m = re.match("^{", line)
        if m:
            state = 'BODY'
        else:
            state = 'BEGIN'
    elif state == 'BODY':
        m = re.match("^\s*?if \((?:\w+equest\.)?fHelp.*?\)$", line)
        if m:
            state = 'HELP'
        else:
            state = 'BEGIN'
    elif state == 'HELP':
        m = re.match("\s*throw (?:std::)?runtime_error\($", line)
        if m:
            state = 'MSG'
        else:
            state = 'BEGIN'
    elif state == 'MSG':
        m = re.match(r"^\s*(\"(.*)\")?(\);)?$", line, re.DOTALL)
        cx = re.match(r"\s*\+ HelpExampleCli\(\"(.*?)\", \"(.*)\"\)$", line)
        rx = re.match(r"\s*\+ HelpExampleRpc\(\"(.*?)\", \"(.*)\"\)$", line)
        if m:
            if m[2]:
                msgs.append(m[2])
            if m[3]:
                close()
                state = 'BEGIN'
        elif cx:
            # CLI Example.
            msgs.append(r"> bitcoin-cli {} {}\n".format(cx[1], cx[2]))
        elif rx:
            # RPC Example.
            msgs.append(r"> curl --user myusername --data-binary '{{\"jsonrpc\": \"1.0\", \"id\":\"curltest\", \"method\": \"{}\", \"params\": [{}] }}' -H 'content-type: text/plain;' http://127.0.0.1:8332/\n".format(rx[1], rx[2]))
        else:
            close()
            state = 'BEGIN'
