#!/usr/bin/env python3
# Generates webpage for an RPC API call, based on its JSON description from STDIN.

import json
import sys

data = json.load(sys.stdin)

html = """
<html>
<head>
    <link rel="stylesheet" type="text/css" href="../../style.css">
</head>
<body>
<h1>{name}</h1>
<h2>{version}</h2>
{message}
</body>
</html>
""".format(**data)
print(html.strip())
