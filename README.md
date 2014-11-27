# names.py

This script reads names from the data file and looks for them in the text file. The first occurrence is left as it is. The second is replaced by the surname. When two authors share a surname their initials are used. When authors share initials full names are used. The format of the data file is CSV and consists of the last name followed by the first name(s). This means that multiple word surnames are allowed.

# acronyms.py

This script looks for the occurrence of phrases in the text file and replaces the first occurrence with the phrase in Markdown emphasis and an abbreviation. Later occurrences are replaced with the abbreviation. The data file is CSV format and stores the phrase followed by an abbreviation.

# duplicates.py

This script looks for duplicated words and reports on which lines they occur.

# atxheaders.py

This script checks that the ATX headers in a Markdown document make sense.
