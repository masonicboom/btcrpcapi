#!/usr/bin/env python3
# Prints stylesheet to stdout.
# Configurable via environment variable MODE. MODE=dark does a dark color scheme; otherwise does a light color scheme.

import os

if "MODE" in os.environ and os.environ["MODE"] == "dark":
    palette = {
        # Colors from https://www.schemecolor.com/apple-rainbow-logo.php.
        "green": "#5EBD3E",
        "blue": "#009CDF",
        "yellow": "#FFB900",
        "orange": "#F78200",
        "red": "#E23838"
    }

    colors = {
        "bg": "black",
        "fg": palette["green"],
        "highlight": "white",
        "present": palette["green"],
        "changed": palette["yellow"],
        "deprecated": palette["blue"]
    }
else:
    palette = {
        # Color codes from https://www.schemecolor.com/rainbow-pastels-color-scheme.php.
        "blue": "#C7CEEA",
        "green": "#B5EAD7",
        "yellow": "#E2F0CB",
        "orange": "#FFDAC1",
        "red": "#FFB7B2"
    }

    colors = {
        "bg": "white",
        "fg": "#333332",
        "highlight": "rgb(247, 142, 35)",
        "present": "#999",
        "changed": palette["red"],
        "deprecated": "#CCC"
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

#legend {{
    margin-top: 3rem;
}}

#legend>table {{
  width: 20rem;
  margin-top: 0;
}}

#legend td:first-child {{
    width: 1rem;
    max-width: 1rem;
}}

td.present {{
    background-color: {present};
    text-align: center;
}}

/* UNCOMMENT FOR DEBUGGING VISUALIZATION td.present a {{ color: pink; }} */

td.present>a {{
    color: {fg};
    opacity: 0;
}}
#chart tr:hover>td.present {{
    opacity: 0.5;
}}
#chart tr:hover>td:hover.present {{
    opacity: 1;
}}
#chart tr:hover>td.present>a {{
    opacity: 1;
    color: {highlight};
}}

td.present.deprecated {{
    background-color: {deprecated};
}}

td.present.msg-changed {{
    background-image: linear-gradient(
        to right top,
        {changed} 33%,
        transparent 33%,
        transparent 66%,
        {changed} 66%
    );
    background-size: 3px 3px;
}}

#chart tbody>tr:hover {{
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