#!/usr/bin/env python3

import argparse
import re

octothorpe_to_depth =\
    {
        '#': 1,
        '##': 2,
        '###': 3,
        '####': 4,
        '#####': 5,
        '######': 6
    }


def get_depth(text, octothorpe_to_depth):
    """ str, dict -> int between 0 and 6
    Take a string and a dictionary representing a mapping of octothorpes to
    depths; return what the current depth of ATX header is.
    >>> get_depth(
        'foo\n# A header\nbar',
        octothorpe_to_depth
    )
    1
    >>> get_depth(
        'foo\n## A header\nbar',
        octothorpe_to_depth
    )
    2
    >>> get_depth(
        'foo\nbar',
        octothorpe_to_depth
    )
    0
    """
    depth = 0
    lines = text.split('\n')
    for line in lines:
        for header in octothorpe_to_depth:
            if re.match('\s{{0,3}}{}\s'.format(header), line):
                depth = octothorpe_to_depth[header]
                break
    return depth


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    args = parser.parse_args()
    target = args.target
    with open(target) as f:
        text = f.readlines()
    depth = 0
    line_number = 1
    for line in text:
        if get_depth(line, octothorpe_to_depth):
            new_depth = get_depth(line, octothorpe_to_depth)
            if abs(depth - new_depth) > 1:
                print(
                    'Big depth change on line {}: from {} to {}'.format(
                        str(line_number),
                        str(depth),
                        str(new_depth)
                    )
                )
            depth = new_depth
        line_number += 1
    if depth == 0:
        print("I didn't find any headers.")
