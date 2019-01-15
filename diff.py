#!/usr/bin/env python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file1")
parser.add_argument("file2")
args = parser.parse_args()

#Adds all lines in two lists, seperated by newlines
f1_lines = open(args.file1).read().split("\n")
f2_lines = open(args.file2).read().split("\n")

output = []
countAdded = 0
countRemoved = 0
#Checks for any common lines.
for line in f2_lines:
    if line == "":
        continue
    elif line in f1_lines:
        output.append("0 " + line)
    else:
        output.append("+ " + line)
        countAdded += 1

count = 0
#Finds every line not in f2. This must have been removed.
for line in f1_lines:
    if line not in f2_lines:
        output.insert(count, "- " + line)
        countRemoved += 1
    count += 1

outfile = open("diff_output.txt", "w+")
print("\nAdded:  ", countAdded)
print("Removed:", countRemoved, "\n")
for str in output:
    outfile.write(str + "\n")
    print(str)
