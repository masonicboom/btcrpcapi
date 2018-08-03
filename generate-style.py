#!/usr/bin/env python3
# Prints stylesheet to stdout.
# Configurable via environment variable MODE. MODE=dark does a dark color scheme; otherwise does a light color scheme.

import os

if "MODE" in os.environ and os.environ["MODE"] == "dark":
    colors = {
        "bg": "black",
        "fg": "green",
        "block": "green",
        "highlight": "white",

        # Color codes from https://www.schemecolor.com/apple-rainbow-logo.php.
        "code-a": "#5EBD3E",
        "code-b": "#009CDF",
        "code-c": "#FFB900",
        "code-d": "#F78200",
        "code-e": "#E23838"
    }
else:
    colors = {
        "bg": "white",
        "fg": "#333332",
        "block": "#aaa",
        "highlight": "rgb(247, 142, 35)",

        # Color codes from https://www.schemecolor.com/rainbow-pastels-color-scheme.php.
        "code-a": "#C7CEEA",
        "code-b": "#B5EAD7",
        "code-c": "#E2F0CB",
        "code-d": "#FFDAC1",
        "code-e": "#FFB7B2"
    }

print("""
body {{
    font-family: monospace;
    background-color: {bg};
    color: {fg};
}}

td {{
    height: 1rem;
}}

td.present {{
    background-color: {block};
    text-align: center;
}}

/* UNCOMMENT FOR DEBUGGING VISUALIZATION td.present a {{ color: pink; }} */

td.present>a {{
    color: {fg};
    opacity: 0;
}}
tr:hover>td.present {{
    opacity: 0.5;
}}
tr:hover>td:hover.present {{
    opacity: 1;
}}
tr:hover>td.present>a {{
    opacity: 1;
    color: {highlight};
}}

td.present.color-a {{
    background-color: {code-a};
}}

td.present.color-b {{
    background-color: {code-b};
}}

td.present.color-c {{
    background-color: {code-c};
}}

td.present.color-d {{
    background-color: {code-d};
}}

td.present.color-e {{
    background-color: {code-e};
}}

tbody>tr:hover {{
    color: {highlight};
}}

.version {{
    width: 1rem;
    writing-mode: vertical-lr;
    transform: rotate(-180deg);
}}

a {{
    color: {fg};
    text-decoration: none;
}}

a:hover {{
    font-weight: bold;
}}

table {{
    margin-top: 5rem;
}}
""".format(**colors).strip())