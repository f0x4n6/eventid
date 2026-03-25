#!/usr/bin/env python3
import json
import sqlite3
import sys


QUERY = """
SELECT provider.name, message.event_id, message.message
FROM messages AS message
INNER JOIN providers AS provider
ON message.provider_id = provider.id
WHERE length(message.message) > 0
ORDER by provider.name, message.event_id;
"""

data, count = dict(), 0


if len(sys.argv) < 2:
    print("usage: generate.py DATABASE")
    sys.exit(2)


with sqlite3.connect(sys.argv[1]) as db:
    cur = db.cursor()
    rows = [row for row in cur.execute(QUERY)]

    last_provider = ""

    for row in rows:
        provider, event_id, message = row

        if last_provider != provider:
            last_provider = provider
            data[provider] = dict()

        # sanitize event message
        message = message.split(". ")[0]

        for i in range(10):
            message = message.replace(f'%{i}', '')

        message = message.replace('"', '')
        message = message.replace("'", '')
        message = message.replace('\\', '')
        message = message.replace('[]', '')
        message = message.replace('()', '')
        message = message.replace('( ', '(')
        message = message.replace(' )', ')')
        message = message.replace(' , ', ' ')
        message = message.replace(' : ', ' ')
        message = message.replace('.: ', '')
        message = message.replace('_: ', '')

        for i in range(5):
            message = message.replace('  ', ' ')

        message = message.strip()
        message = message.removesuffix(".")
        message = message.removesuffix("-")
        message = message.removesuffix(":")

        if len(message) > 8:
            data[provider][int(event_id)] = message
            count += 1


with open("events.csv", "w+") as file:
    for provider, events in data.items():
        for event_id, message in events.items():
            file.write(f'"{provider}",{event_id},"{message}"\n')


with open("events.json", "w+") as file:
    file.write(json.dumps(data, sort_keys=True, indent=2))


with open("events.go", "w+") as file:
    file.write('package events\n\n')
    file.write('var Events = map[string]map[int64]string{\n')

    for provider, events in data.items():
        if len(events) == 0:
            continue

        file.write(f'    "{provider.strip()}": {{\n')

        for event_id, message in events.items():
            file.write(f'        {event_id}: "{message.strip()}",\n')

        file.write('    },\n')
    file.write('}\n')


print(f'Generated {count} event messages')
