#!/usr/bin/env python
import sys

def foo(var1, bar):
    print(None, True, False, None, None)
    print(123, "an 1nt3g3r string", 123, var1)

    while var1 != "False":
        var1 = "False"

    while "False" == var1:
        print("Hello World!\n")
        var1 = 100


very_important_variable = 10       #This is a comment

while very_important_variable < 10:      #another comment
    print("This is a string", "this is another string")
    very_important_variable += 1

foo("123", very_important_variable)  #final comment

multiLine_String = "\nline1\n line2 None end True\n of False string"
