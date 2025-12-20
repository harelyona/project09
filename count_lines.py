import os
import re
from pathlib import Path

# 1. Regex to identify comments
REMOVE_COMMENTS = re.compile(
    r'/\*.*?\*/|//[^\n]*',
    re.S
)

# 2. Regex to remove "structural" characters to check if a line is empty
# (Removes spaces, tabs, braces, and parentheses)
REMOVE_STRUCTURE = re.compile(r'[ \t\{\}\(\)]')

# 3. Keywords that identify "fluff" lines (declarations/definitions)
FLUFF_KEYWORDS = {
    'class', 'constructor', 'function', 'method',
    'field', 'static', 'var'
}

PATH = Path(os.getcwd())
JACK = '*.jack'

total_lines = 0

for file in PATH.glob(JACK):
    with file.open() as f:
        content = f.read()

    # Step 1: Remove all comments from the file content first
    content_no_comments = REMOVE_COMMENTS.sub('', content)

    file_count = 0
    lines = content_no_comments.splitlines()

    for line in lines:
        stripped_line = line.strip()

        # Skip empty lines
        if not stripped_line:
            continue

        # Get the first word to check if it is a declaration keyword
        # .split()[0] handles both spaces and tabs automatically
        first_word = stripped_line.split()[0]

        # Step 2: Skip Declaration lines
        if first_word in FLUFF_KEYWORDS:
            continue

        # Step 3: Skip Bitmap printing code (Memory.poke)
        if 'Memory.poke' in stripped_line:
            continue

        # Step 4: Remove structural chars ({ } ( ) space)
        # If nothing is left (e.g., the line was just "}"), don't count it.
        cleaned_line = REMOVE_STRUCTURE.sub('', stripped_line)

        if cleaned_line:
            file_count += 1

    print(f'{file.name}: {file_count}')
    total_lines += file_count

print(f'\nTOTAL MEANINGFUL LINES: {total_lines}')