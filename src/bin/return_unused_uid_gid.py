#!/usr/bin/env python3

users = {}
groups = {}
with open("/etc/passwd", "r", encoding="UTF-8") as f:
    for line in f.readlines():
        line_split = line.split(":")
        users[line_split[2]] = line_split[0]
        groups[line_split[3]] = line_split[0]

uuid = 0
for i in range(800, 1000):
    if users.get(str(i)) is None:
        uuid = i
        break

ugid = 0
for i in range(800, 1000):
    if groups.get(str(i)) is None:
        ugid = i
        break

if uuid > 0 and ugid > 0:
    print("uuid", uuid)
    print("ugid", ugid)
