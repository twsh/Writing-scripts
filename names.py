#!/usr/bin/env python3

import argparse
import csv
import re
import shutil


def check_dictionary_for_duplicates(dictionary):
    """ dict -> list of str
    Take a dictionary, return a string consisting of the 'name' element
    of the value tuples iff that tuple appears as a value more than once.
    >>> check_dictionary_for_duplicates(
        {
            'Smith1': ('John Smith', 'John Smith'),
            'Smith2': ('John Smith', 'John Smith')
        }
    )
    ['John Smith']
    >>> check_dictionary_for_duplicates(
        {
            'Smith1': ('John Smith', 'John Smith'),
            'Smith2': ('Jane Smith', 'Jane Smith')
        }
    )
    None
    """
    values = [dictionary[x] for x in dictionary]
    duplicate_names = list(set([x[1] for x in values if values.count(x) > 1]))
    if duplicate_names:
        return duplicate_names


def split_name(name):
    """ list of str -> tuple of str
    Take a list of strings (a surname and forenames)
    and return a tuple containing:
    *   The full name (forename + surname)
    *   The surname
    *   The initials: a string consisting of the first letters of forenames
        separated by a full stop ('.') and a space.
    Case is preserved (which makes 'bell hooks' possible).
    >>> split_name(['Hodgson', 'Thomas William Strickland'])
    ('Thomas William Strickland Hodgson', 'Hodgson', 'T. W. S.')
    >>> split_name(['Strickland Hodgson', 'Thomas William'])
    ('Thomas William Strickland Hodgson', 'Strickland Hodgson', 'T. W.')
    """
    surname = re.sub('\s+', ' ', name[0].strip())
    forenames = re.sub('\s+', ' ', name[1].strip())
    fullname = '{} {}'.format(forenames, surname)
    initials = ' '.join([x[0] + '.' for x in forenames.split()])
    return fullname, surname, initials


def make_name_dictionary(csvfile):
    """ file ready to read -> dict
    Take a file open for reading, assuming it is in CSV format and each row
    is a name in the form 'surname', 'forename'.
    Return a dictionary where each key is a surname and each value
    is a tuple of the full name and the surname.
    Where the surnames are not unique the key will have a number appended,
    and the second element of the tuple will be the surname
    with initials prepended.
    """
    data = csv.reader(csvfile)
    list_of_split_names = [split_name(row) for row in data]
    list_of_surnames = [x[1] for x in list_of_split_names]
    unique_surnames = [x for x in list_of_surnames if list_of_surnames.count(x) == 1]
    # Make a dictionary from the unique surnames first.
    dictionary = {x[1]: (x[0], x[1]) for x in list_of_split_names if x[1] in unique_surnames}
    # Now handle the trickier case of non-unique surnames.
    non_unique_surnames = list(set([x for x in list_of_surnames if list_of_surnames.count(x) > 1]))
    for dup in non_unique_surnames:
        list_of_initials = [x[2] for x in list_of_split_names if x[1] == dup]
        non_unique_initials = list(set([x for x in list_of_initials if list_of_initials.count(x) > 1]))
        i = 1
        for name in list_of_split_names:
            fullname = name[0]
            surname = name[1]
            initials = name[2]
            if surname == dup:
                key = surname + str(i)
                i += 1
                if initials in non_unique_initials:
                    dictionary[key] = fullname, fullname
                else:
                    dictionary[key] = fullname, '{} {}'.format(initials, surname)
    if dictionary:
        return dictionary

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    parser.add_argument('names')
    args = parser.parse_args()
    target = args.target
    names = args.names
    with open(names) as f:
        dictionary_of_names = make_name_dictionary(f)
    shutil.copy(target, target + '.backup')
    print(
        "I have made a backup of the orignal file at {}.backup"
        .format(target)
    )
    duplicate_names = check_dictionary_for_duplicates(
        dictionary_of_names
    )
    if duplicate_names:
        print(
            'Some names were repeated in {}: {}.'.format(
                names,
                ', '.join(duplicate_names)
            )
        )
    with open(target) as f:
        text = f.read()
    for key in dictionary_of_names:
        try:
            first_occurrence = text.index(dictionary_of_names[key][0])
        except ValueError:
            print("The name '{}' wasn't in {}".format(
                dictionary_of_names[key][0],
                target)
            )
        else:
            text = (
                text[:first_occurrence+len(dictionary_of_names[key][0])]
                + re.sub(
                    dictionary_of_names[key][0],
                    dictionary_of_names[key][1],
                    text[first_occurrence+len(dictionary_of_names[key][0]):]
                )
            )
    with open(target, 'w') as f:
        f.write(text)
