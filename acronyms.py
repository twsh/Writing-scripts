#!/usr/bin/env python3

import argparse
import csv
import os
import re
import shutil


class ExtensionError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def check_extensions(p, l):
    """ str, list of str -> string, bool
    Take a path and a list of strings.
    If the path has one of the list as an extension,
    return the path.
    If the path has another extension,
    raise an ExtensionError.
    If the path has no extension, check the list in order for files with that
    extension then return the path with the first one added.
    If a file isn't found, raise an ExtensionError.
    >> check_extensions('foo.txt', ['txt'])
    'foo.txt'
    >> check_extensions('foo.md', ['txt'])
    None
    >> check_extensions('foo', ['txt'])
    'foo.txt'
    """
    if os.path.splitext(p)[1][1:] in l:
        return p
    elif os.path.splitext(p)[1]:
        message = ("I know about these extensions: {}. "
                   "You have chosen an extension I don't know about: {}."
                   .format(', '.join(l), os.path.splitext(p)[1][1:]))
        raise ExtensionError(message)
    else:
        for i in range(len(l)):
            if os.path.isfile(p + '.' + l[i]):
                return p + '.' + l[i]
            else:
                message = ("I know about these extensions: {}. "
                           "I couldn't find a file with one of these "
                           "extensions."
                           .format(', '.join(l)))
                raise ExtensionError(message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    parser.add_argument('acronyms')
    args = parser.parse_args()
    target = args.target
    acronyms = args.acronyms
    shutil.copy(target, target + '.backup')
    print(
        "I have made a backup of the orignal file at {}.backup."
        .format(target)
    )
    list_of_extensions_acronyms = ['txt']
    txt = check_extensions(acronyms, list_of_extensions_acronyms)
    # The text file to read acronyms from
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
