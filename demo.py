#!/usr/bin/env python
import numpy

def foo(var1, bar):
    print(None, True, False, None, None)
    print(123, "an 1nt3g3r string", 123, var1)

    while var1 != "False":
        var1 = "False"

    while "False" == var1:
        var1 = 100
        print("Hello World!\n")


very_important_variable = 0        #This is an assignment = 123 comment

while very_important_variable < 10:      #another comment
    print("This is a string", "this is another string")
    very_important_variable += 1

foo("123", very_important_variable)  #final comment

print(very_important_variable)

multiLine_String = "\nline1\n line2 None end True\n of False string"
