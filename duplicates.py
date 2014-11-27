#!/usr/bin/env python3

import argparse
import re


def split_line_into_words(line):
    """ str -> list of str
    Take a string (representing a line of text) and
    return a list of the words in the line.
    All words will be in lower case, and punctuation will be removed.
    (The list comprehensions are to deal with the punctuation marks picked up
    by the regex.)
    >>> split_line_into_words('Foo? Bar!\n')
    ['foo', 'bar']
    """
    return [x for x in re.split('\W*', line.lower().strip()) if x]


def check_string_for_duplicates(s):
    """ str -> str
    Take a string and split into words, i.e. at spaces and punctuation.
    Return a string consisting of all the words that are identical
    to the next word.
    The strings will have single quotes around them.
    >>> check_string_for_duplicates('Foo foo.')
    "'Foo'"
    >>> check_string_for_duplicates('Foo foo, bar Bar.')
    "'Foo', 'bar'"
    >>> check_string_for_duplicates('Foo bar.')
    ''
    """
    list_of_words = split_line_into_words(s)
    return ', '.join(
        ["'{}'".format(x) for i, x in enumerate(list_of_words[:-1])
            if x == list_of_words[i+1]]
    )


def compare_line_edges(line1, line2):
    """
    str, str -> str
    Take two strings (i.e. lines of text).
    Compare the last word of line 1 to the first word of line 2.
    If they are the same, then return that word.
    Case and punctuation are ignored.
    >>> compare_line_edges('Foo bar.', 'Bar foo.')
    'bar'
    >>> compare_line_edges('Foo foo.', 'Bar bar.')
    None
    """
    line1_words = split_line_into_words(line1)
    line2_words = split_line_into_words(line2)
    # I need to check that the line wasn't empty,
    # because otherwise indexing the list will fail.
    if line1_words:
        end_word = split_line_into_words(line1)[-1]
    if line2_words:
        beginning_word = split_line_into_words(line2)[0]
    if line1_words and line2_words and end_word == beginning_word:
        return "'{}'".format(end_word)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    args = parser.parse_args()
    target = args.target
    with open(target) as f:
        dictionary_of_lines = dict(enumerate(f.readlines(), start=1))
    for key in dictionary_of_lines:
        duplicates = check_string_for_duplicates(
            dictionary_of_lines[key]
        )
        if duplicates:
            print('{} on line {}'.format(duplicates, key))
        if key+1 in dictionary_of_lines:
            if compare_line_edges(
                dictionary_of_lines[key],
                dictionary_of_lines[key+1]
            ):
                print('The last word of line {} ({}) '
                    'is the same as the first word of line {}.'.format(
                        key,
                        compare_line_edges(
                            dictionary_of_lines[key],
                            dictionary_of_lines[key+1]
                        ),
                        key+1
                    )
                )
