#!/usr/bin/env python3

import os

RULE_NAME = "DCPomaticRemote"

command = os.popen(f"ufw status numbered | grep {RULE_NAME}")
commands_out = command.readlines()

rules = []
for out in commands_out:
    if not out.strip():
        continue
    rule_splitted = out.strip().split()
    rule_num = rule_splitted[0] if rule_splitted[0] != "[" else rule_splitted[1]

    rule_num = rule_num.strip("[] \n\r")
    rules.append(rule_num)

rules.sort(reverse=True)

for rule in rules:
    os.popen(f"ufw --force delete {rule}").readlines()
