This directory contains 5 scripts, whereas 3 of them are demo files.
This document will cover the scripts: "highlighter.py", "grep.py" and "diff.py"



1. highlighter.py:

	1.1: Type "python3 highlighter.py [python.syntax|naython.syntax] [python.theme|naython.theme] <filename>"
	     to run this script

	1.2: demo.py is used as a testfile and printed in stdout with the colors made by highlighter.py

	1.3: The script will first translate the .syntax and .theme files into directories
	     Then it will perform a search through each line in the file, and color the line accordingly
	     The search uses regular expressions, defined in the .syntax file to find out what color to use.
	     Finally the script prints out the colorized line.

	1.4: I have assumed the \n and \t characters can only occur in strings.
	     Also to add support for naython, all tests are enclosed in try-except blocks.
	     I had some trouble doing overlaps, but found a somewhat messy solution, but hey
	     - as long as it works!

	1.5: The program doesn't support every edge case and statement, e.g. function calls in while statements.


2. grep.py:

	2.1: Type "python3 grep.py (regular-expressions) <filename> [--highlight]" to run this script

	2.2: Just like highlighter.py, uses a dictionary with all the themes available. Cycles between 
	     red, green, yellow, blue, magenta, and cyan colors. Uses regular expressions as key.

	2.3: Will use all regular expressions provided and search through the file. Prints out the line
	     if match is found. If --highlight provided, colors the matches with different colors. 


3. diff.py:

	3.1: Type "python3 diff.py [diffA.txt | demo.py] [diffB.txt | demo2.py]" to run this script

	3.2: Once run, the output will be written to a new file called diff_output.txt

	3.3: Takes two files as input, whereas the first file is the original and the second is modified

	3.4: First the program takes all the lines in both files and stores them in lists.
	     Then it creates an empty "output" list, where every common line in both lists are added with a 0.
	     Every line in list 2 not in list 1 are added with a +. These lines can't exist in list 1, thus
	     making it an "added" line. It then does the same for list 1, where every line not in list 2 must've
	     been removed. Finally this output list is printed out.
	
	3.5: The output file can be used in highlighter.py to color all additions with green and all
	     removals with red. Use "python3 highlighter.py diff.syntax diff.theme diff_output.txt" to do this.


4. REGULAR EXPRESSIONS

	4.1: I have found the regular expressions difficult to write and even harder to read, so I'll try my
	     best to explain them here.

	4.2: "#.*(?:$|\n)": comment
		
		4.2.1: Pretty straight forward. A comment starts with # and lasts to the end of the line.

	4.3: "(\s*print)\s*(\((?:[\"\'\s].*[\"\'\s]|\w*)(?:,\s*(?:[\"\'\s].*[\"\'\s]|\w*))*\))\s*": print

		4.3.1: Group 1: (\s*print) checks that it starts with print

		4.3.2: Group 2: (?:[\"\'\s].*[\"\'\s]|\w*) checks if a string is provided or a variable

		4.3.3: Group 3: (?:,\s*(?:[\"\'\s].*[\"\'\s]|\w*))* same as group 2, but starts with ',' and
		       can have 0 or more

	4.4: "^(\s*\w+\s*)(\((?:[\"\'].*[\"\']|\w+)?(?:(?:,\s*)(?:[\"\'].*[\"\']|\w+))*\)\s*)": function

		4.4.1: Does the same as print, but the beginning, (\s*\w+\s*) checks for any set of characters.

	4.5: "^(\s*def\s*)(\w*)(\((?:\w*(?:,\s?\w*)*)\):)": define
	
		4.5.1: Group 1: ^(\s*def\s) checks that a statement starts with def
		4.5.2: Group 2: (\w*) checks for any word characters. This is the function name
		4.5.3: Group 3: (\((?:\w*(?:,\s?\w*)*)\):) are the arguments, enclosed by paranteses and 
		       ends with colon.

	4.6: "^import\s*\w*\s*": import

		4.6.1: Fairly easy to read. Starts with "import", followed by any wordcharacter.

	4.7: "(\s*[a-zA-Z]\w*\s*[+=\-\*]{1,2})(\s*(?:[\'\"].*[\'\"]|\w+)\s*)": assignment

		4.7.1: Group 1: (\s*[a-zA-Z]\w*\s*[+=\-\*]{1,2}) checks that a variable is put together by a
		       letter followed by any word character. Then there is either one or two assignment 
		       characters; +, =, -, *. A bug here is that it accepts e.g *+. 

		4.7.2: Group 2: (\s*(?:[\'\"].*[\'\"]|\w+)\s*) this group is used often. It checks for a string
		       or a variable. 

	4.8: "(while)(\s*(?:[\"\'].*?[\"\']|\w*)\s*(?:[!<>=]{1,2}\s*(?:[\"\'].*?[\"\']|\w*))?:\s*)": while

		4.8.1: Group 1: (while). Checks that the string starts with "while".

		4.8.2: Group 2: (?:[\"\'].*?[\"\']|\w*) Checks for a string or a variable

		4.8.3: Group 3: (?:[!<>=]{1,2}\s*(?:[\"\'].*?[\"\']|\w*)) Assumes group 2 is followed by one or 
		       two boolean operators. Then another check for variable or string.

	4.9: "([\"\'].*?[\"\'])": string
		
		4.9.1: Checks for a string. This group is seen alot in the other regular expressions.

	4.10: "\b\d+\b": number
		4.10.1: Checks for a number. Must be a digit in the beginning and end of a word

	4.11: "\bNone\b|\bTrue\b|\bFalse\b": special
		4.11.1: Checks for a special statement None or True or False.

	4.12: "\\t|\\n": general
		4.12.1: Checks for the special character \n newline or \t tabs.
