#! /usr/bin/env python

# previous line was /usr/local/bin/python, but that might not be where your python lives.

import re
import argparse

# Create an argument parser and tell it about arguments
parser = argparse.ArgumentParser(description = 'Make code tidier.')

# positional argument for input file
parser.add_argument(
  '-f', '--file', metavar = "<file name>",
  help = 'name of input file')

# named argument for output file
parser.add_argument(
  '-o', '--out', dest = 'out_file', default = None,
  metavar = "<file name>",
  help = 'name of output file (default: use stdout)')

# spaces per tab; defaults to 4; must be an integer
parser.add_argument(
  '-t', '--tab-spaces', dest = 'tab_spaces', default = 4,
  type = int, metavar = "<integer>",
  help = 'number of spaces to use for each tab at the start of a line')

# comment characters
parser.add_argument(
  '-c', '--comment', dest = 'comment_chars', default = "#,//",
  metavar = "<comma separated list of comment characters>",
  help = 'strings to be interpreted as starting coded comments'
  )

# boolean arguments, aka flags
parser.add_argument(
  '-p', '--python',
  dest = 'python', action = "store_true",
  help = 'Tidy with python rules')

parser.add_argument(
  '-r', '--report',
  dest = 'report', action = "store_true",
  help = 'Instead of fixing the file, generate a report listing issues.')

parser.add_argument(
  '-x', '--extra',
  dest = 'extra', action = "store_true",
  help = 'Use extra features')

args = parser.parse_args()
print(args)
comment_chars = args.comment_chars.split(",")
print(comment_chars)

# This reads the entire file all at once.
# You could also read it line by line.

f = open(args.file)
contents = f.read()

modified_contents = contents

# This stub just capitalizes all c's, a's, l's, v's, i's, and n's.
# Delete these and add in your own regex substitutions.

modified_contents = re.sub(r'c', r'C', modified_contents)
modified_contents = re.sub(r'a', r'A', modified_contents)
modified_contents = re.sub(r'l', r'L', modified_contents)
modified_contents = re.sub(r'v', r'V', modified_contents)
modified_contents = re.sub(r'i', r'I', modified_contents)
modified_contents = re.sub(r'n', r'N', modified_contents)

# Capitlize p's too if --python is set.
if args.python:
    modified_contents = re.sub(r'p', r'P', modified_contents)

if args.out_file:
    outf = open(args.out_file, "w")
    outf.write(modified_contents)
else:
    print(modified_contents)