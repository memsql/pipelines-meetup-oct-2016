#!/usr/bin/python3

import json
import os
import re
import struct
import sys


# This is a bit of boilerplate that handles the way that incoming records are
# encoded. Data is streamed to stdin, and each record is prefixed with 8 bytes
# indicating how long the record is. This Python generator reads individual
# records and yields them one by one.
def transform_records():
    while True:
        byte_len = sys.stdin.buffer.read(8)
        if len(byte_len) == 8:
            byte_len = struct.unpack("L", byte_len)[0]
            result = sys.stdin.buffer.read(byte_len)
            yield result.decode("utf-8", "replace")
        else:
            assert len(byte_len) == 0, byte_len
            return


# Iterate over the records that we receive from Kafka.
for line in transform_records():

    (id, timestamp, retweet_count, favorite_count, username, body) = line.split("\t")

    pattern = re.compile(r"@\w{1,15}", re.ASCII)
    linked_usernames = re.finditer(pattern, body)

    for link in linked_usernames:
        sys.stdout.write(username)
        sys.stdout.write("\t")
        sys.stdout.write(link.group(0)[1:])
        sys.stdout.write("\n")
