#!/usr/bin/env python3
# Processes API call lists for each bitcoin version into dataset containing API call, earliest release it appeared in, and latest release it appeared in.

import os

earliest = {}
latest = {}
calls = set()

versions = []
for fn in os.listdir('apis/'):
    if fn == 'master':
        continue

    v = [int(x) for x in fn[1:].split('.')]
    versions.append(v)

def process_version(v):
    f = open('apis/{}'.format(v), 'r')
    for line in f.readlines():
        call = line.rstrip()

        calls.add(call)
        if call not in earliest:
            earliest[call] = v
        latest[call] = v

for vl in sorted(versions):
    v = 'v{}'.format('.'.join([str(v) for v in vl]))
    process_version(v)

process_version('master')

print('|call|earliest|latest|')
print('|----|--------|------|')
for call in sorted(calls):
    print('|{}|{}|{}|'.format(call, earliest[call], latest[call]))
