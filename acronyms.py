#!/usr/bin/env python3

import argparse
import csv
import os
import re
import shutil


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    parser.add_argument('acronyms')
    args = parser.parse_args()
    target = args.target
    txt = args.acronyms
    shutil.copy(target, target + '.backup')
    print(
        "I have made a backup of the orignal file at {}.backup."
        .format(target)
    )
    with open(txt) as f:
        list_of_acronyms = [row for row in csv.reader(f)]
    with open(target) as f:
        text = f.read()
    for acronym in list_of_acronyms:
        full = re.sub('\s+', ' ', acronym[0].lower())
        letters = acronym[1].strip().upper()
        try:
            first_occurrence = text.lower().index(full)
            if text[first_occurrence].isupper():
                full = full[0].upper() + full[1:]
            text = (
                text[:first_occurrence]
                + '*{}* ({})'.format(full, letters)
                + re.sub(
                    full,
                    letters,
                    text[first_occurrence + len(full):],
                    flags=re.I
                )
            )
        except ValueError:
            print("'{}' wasn't found.".format(full))
    with open(target, 'w') as f:
        f.write(text)
