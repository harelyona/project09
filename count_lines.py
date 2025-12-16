import os
import re
from pathlib import Path

NOT_IMPORTANT = re.compile(
	r'/\*.*?\*/|//[^\n]*|[ \{\}\(\)]',
	re.S
)
PATH = Path(os.getcwd())
JACK = '*.jack'

counter = 0
for file in PATH.glob(JACK):
	with file.open() as f:
		content = f.read()
	lines = NOT_IMPORTANT.sub('', content).splitlines()
	count = len(list(filter(None, lines)))
	print(f'{file.name}: {count}')
	counter += count

print(f'\nTOTAL: {counter}')
