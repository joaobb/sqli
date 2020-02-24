import sys
import time

def spinning_cursor():
	while True:
		for cursor in '|/-\\':
			yield cursor

def loading(title):
	spinner = spinning_cursor()
	print(title)
	while True:
		sys.stdout.write(next(spinner))
		sys.stdout.flush()
		time.sleep(0.3)
		sys.stdout.write('\b')

