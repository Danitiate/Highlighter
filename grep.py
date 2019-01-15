#!/usr/bin/env python
import argparse
import re

def colorize(string, matches, color):
    "Colors all the matches found"
    for match in matches:
        string = string.replace(match, "\033[{}m".format(color) + match + "\033[0m")
    return string

parser = argparse.ArgumentParser()
parser.add_argument("regex", nargs="+", help="regular expression")
parser.add_argument("filename", help="file")
parser.add_argument("--highlight", nargs='?', default=0, help="colors the matching lines")
args = parser.parse_args()

theme = {}
colorValue = 91
for regex in args.regex:
    key = regex
    val = colorValue
    theme[key] = val
    colorValue += 1
    if(colorValue > 96): #cycles colors red, green, yellow, blue, magenta, cyan
        colorValue = 91

with open(args.filename) as f:
    for line in f:
        found = False
        line = line.rstrip()
        for regex in args.regex:
            if re.search(regex, line):
                found = True
                if(args.highlight == None): #if --highlight is provided
                    matches = re.findall(regex, line)
                    line = colorize(line, matches, theme[regex])
        if found: #only prints if a string has been found
            print(line)
