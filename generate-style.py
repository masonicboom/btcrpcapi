#!/usr/bin/env python3
# Prints stylesheet to stdout.
# Configurable via environment variable MODE. MODE=dark does a dark color scheme; otherwise does a light color scheme.

import os

if "MODE" in os.environ and os.environ["MODE"] == "dark":
    colors = {
        "bg": "black",
        "fg": "green",
        "block": "green",
        "highlight": "white"
    }
else:
    colors = {
        "bg": "white",
        "fg": "#333332",
        "block": "#aaa",
        "highlight": "rgb(247, 142, 35)"
    }

print("""
body {{
    font-family: monospace;
    /* background-color: black;
    color: green; */
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
    color: {block};
}}
tr:hover>td.present>a {{
    color: {fg};
}}
tbody>tr:hover>td.present {{
    background-color: {highlight};
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