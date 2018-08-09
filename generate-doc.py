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
""".format(**data)
print(html.strip())
