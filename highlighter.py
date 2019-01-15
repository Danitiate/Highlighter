#!/usr/bin/env python
import sys
import re


def argumentOverlap(args, syntax, theme):
    """
    Colors arguments with the correct color to prevent overlap issues.
    Takes args and the syntax- and theme dictionaries as parameters
    Returns the arguments with pretty colors
    """
    end_code = "\033[0m"
    strings = re.findall(syntax["string"], args)
    numbers = re.findall(syntax["number"], args)
    special = re.findall(syntax["special"], args)
    generals = re.findall(syntax["general"], args)

    for w in strings:
        args = args.replace(w, "\033[{}m".format(theme["string"]) + w + end_code)

    for x in numbers: #Checks if a number is in a string or not
        if not strings:
            args = args.replace(x, "\033[{}m".format(theme["variable"])\
                   + x + end_code)
        for w in strings:
            if w.find(x) != -1:
                args = args.replace(x, "\033[{}m".format(theme["string"]) + x)
            else:
                args = args.replace(x, "\033[{}m".format(theme["variable"])\
                       + x + end_code)

    for y in special: #Checks if a special value is in a string or not
        if not strings:
            args = args.replace(y, "\033[{}m".format(theme["variable"])\
                   + y + end_code)
        for w in strings:
            if w.find(y) != -1:
                args = args.replace(y, "\033[{}m".format(theme["variable"])\
                       + y + end_code + "\033[{}m".format(theme["string"]))
            else:
                args = args.replace(y, "\033[{}m".format(theme["variable"])\
                       + y + end_code)

    for z in generals: #Assumes special characters are always in a string
        args = args.replace(z, "\033[{}m".format(theme["special"]) + z + end_code + "\033[{}m".format(theme["string"]))

    return args


def check_color(string, syntax, theme, color):
    """
    Uses a set of rules to color a line sent from check_syntax
    Parameters: the string to be colored. Uses the dictionaries syntax and theme
                to find the correct color. Uses the rules from param color.
    Returns: The string with new colors
    """
    end_code = "\033[0m"

    if color == "print":
        code = theme["print"]
        start_code = "\033[{}m".format(code)
        (a, b) = string #(print)(args)
        a += "\033[0m"
        b = argumentOverlap(b, syntax, theme)
        string = a + b

    elif color == "comment":
        code = theme["comment"]
        start_code = "\033[{}m".format(code)

    elif color == "define":
        code = theme["define"]
        start_code = "\033[{}m".format(code)

        (a, b, c) = string #(def) (func) (param)
        a += end_code
        b = "\033[{}m".format(theme["function"]) + b + end_code

        variables = re.findall(r"\w+", c)
        for x in variables:
            c = c.replace(x, "\033[{}m".format(theme["variable"]) + x + end_code)

        string = a + b + c

    elif color == "function":
        code = theme["function"]
        start_code = "\033[{}m".format(code)
        (a, b) = string #(func)(param)
        a += "\033[0m"
        b = argumentOverlap(b, syntax, theme)
        string = a + b

    elif color == "while":
        code = theme["while"]
        start_code = "\033[{}m".format(code)
        (a, b) = string #(while)(condition)
        a += end_code
        b = argumentOverlap(b, syntax, theme)
        string = a + b

    elif color == "assignment":
        start_code = ""
        (a, b) = string #(var =)(value)
        b = argumentOverlap(b, syntax, theme)
        string = a + b


    elif color == "import":
        code = theme["import"]
        start_code = "\033[{}m".format(code)

        (a,b) = string.split() #(import)(class)
        a = string[:string.find(b)]
        a += end_code
        string = a + b
        return start_code + string

    string = string.rstrip("\n")
    return start_code + string + end_code


def check_syntax(string, syntax, theme):
    """
    Uses regular expressions, defined in syntax, to find what type of line we're
    dealing with. Will then find all the matches in a line and send it to
    check_color() to colorize the matches accordingly.

    Takes a line as input, as well as the dictionaries syntax and theme.

    Returns the line with new, pretty colors.
    """

    result = ""
    #Adds support for coloring diff
    try:
        if re.search(syntax["added"], string):
            code = theme["added"]
            return "\033[{}m".format(code) + string.strip() + "\033[0m"
    except KeyError:
        pass

    try:
        if re.search(syntax["removed"], string):
            code = theme["removed"]
            return "\033[{}m".format(code) + string.strip() + "\033[0m"
    except KeyError:
        pass

    try:
        if re.search(syntax["match"], string):
            return string.strip()
    except KeyError:
        pass

    #Function needs to be colored before print
    try:
        if re.search(syntax["function"], string):
            matches = re.findall(syntax["function"], string)
            result = check_color(matches[0], syntax, theme, "function")
    except KeyError:
        pass

    try:
        if re.search(syntax["print"], string):
            matches = re.findall(syntax["print"], string)
            result = check_color(matches[0], syntax, theme, "print")
    except KeyError:
        pass

    try:
        if re.search(syntax["define"], string):
            matches = re.findall(syntax["define"], string)
            result = check_color(matches[0], syntax, theme, "define")
    except KeyError:
        pass

    try:
        if re.search(syntax["import"], string):
            substring = ""
            matches = re.findall(syntax["import"], string)
            for str in matches:
                substring += str
            result += check_color(substring, syntax, theme, "import")
    except KeyError:
        pass

    try:
        if re.search(syntax["while"], string):
            matches = re.findall(syntax["while"], string)
            result += check_color(matches[0], syntax, theme, "while")
    except KeyError:
        pass

    try:
        if re.search(syntax["assignment"], string):
            substring = ""
            matches = re.findall(syntax["assignment"], string)
            result += check_color(matches[0], syntax, theme, "assignment")
    except KeyError:
        pass

    #comment needs to be last
    try:
        if re.search(syntax["comment"], string):
            substring = ""
            matches = re.findall(syntax["comment"], string)

            for str in matches:
                substring += str
            result += check_color(substring, syntax, theme, "comment")
    except KeyError:
        pass


    return result


#Saves theme and syntax values in a directory for easier access
syntax = {}
with open(sys.argv[1]) as s:
    for line in s:
        (val, key) = line.split()
        val = val[1:-2] #ignores quotation marks
        syntax[key] = val

theme = {}
with open(sys.argv[2]) as t:
    for line in t:
        (key, val) = line.split()
        key = key[:-1]
        theme[key] = val

#Prints the file with colors
with open(sys.argv[3]) as f:
    for line in f:
        out = check_syntax(line, syntax, theme)
        print(out)
