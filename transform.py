#!/usr/bin/python

import re
import struct
import sys

RE_TWITTER_USERNAME = re.compile(r"@\w{1,15}")


# This is a bit of boilerplate that handles the way that incoming records are
# encoded. Data is streamed to stdin, and each record is prefixed with 8 bytes
# indicating how long the record is. This Python generator reads individual
# records and yields them one by one.
def transform_records():
    while True:
        byte_len = sys.stdin.read(8)
        if len(byte_len) == 8:
            byte_len = struct.unpack("L", byte_len)[0]
            result = sys.stdin.read(byte_len)
            yield result.decode("utf-8", "replace")
        else:
            assert len(byte_len) == 0, byte_len
            return


# Iterate over the records that we receive from Kafka.
for line in transform_records():
    (tid, _, _, _, username, body) = line.split("\t")

    for link in re.finditer(RE_TWITTER_USERNAME, body):
        sys.stdout.write(tid)
        sys.stdout.write("\t")
        sys.stdout.write(username)
        sys.stdout.write("\t")
        # The [1:] is to strip the @ sign
        sys.stdout.write(link.group(0)[1:])
        sys.stdout.write("\n")
