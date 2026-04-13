#!/usr/bin/env python3
"""
MIT License

Copyright (c) 2026 Fox Forensics

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import json
import sqlite3
import sys

from compression import zstd


def declutter(msg: str) -> str:
    msg = msg.split(". ")[0]
    msg = msg.replace("  ", " ")
    msg = msg.removesuffix(".")

    return msg.strip()


def build() -> int:
    data, last, n = {}, "", 0

    with sqlite3.connect("assets/welm_combined.db") as db:
        for row in [row for row in db.cursor().execute("""
        SELECT provider.name, message.event_id, message.message FROM messages AS message
        INNER JOIN providers AS provider ON message.provider_id = provider.id
        WHERE length(message.message) > 0
        ORDER by provider.name, message.event_id;
        """)]:
            provider, event_id, message = row

            if last != provider:
                last = provider
                data[provider] = {}

            message = declutter(message)

            if len(message) > 2:
                data[provider][int(event_id)] = message
                n += 1

    with zstd.open("db.zst", "w") as f:
        f.write(json.dumps(data, sort_keys=True).encode("utf-8"))

    return n


def main(script, *args):
    print(f"[*] Build database with {build()} event messages")


if __name__ == "__main__":
    sys.exit(main(*sys.argv))
