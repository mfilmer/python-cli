python-cli
==========

A python module to simplify writing programs driven through a command line interface

Overview
--------

This module is designed to assist in writing programs where the main interface to the program is a command line. At this command line, users enter commands and these commands trigger function calls from within this module. 

Methods
-------

The following are the public methods:
1. addCommand()
2. delCommand()
3. setPrompt()
4. setNoMatch()
5. setExit()
6. run()

These commands allow the developer to set up patterns for user entered commands. When a command matches a pattern, it triggers a function call. The function gets the original command line passed to it, along with extracted data as defined in the pattern.

###addCommand(pattern,function)

Other than run(), this is the most important method. It is what defines new 
patterns for user entered commands and specifies the function that should be 
called when the pattern is matched. 

###setPrompt(prompt)

The prompt specified should be a function that returns a string. This function 
is called every time a prompt is to be displayed. The default prompt function 
is: `lambda : '> '`

###setNoMatch(function)

The no match function is the function called if there is no matching pattern found. The default no match function is:
lambda x,y: print('Invalid command')

The no match function must take exactly two parameters. The first is the command line entered by the user. The second is the cli object. 

###setExit(exitPatterns)

This method sets the patterns that will cause the run loop to exit. These patterns can be any valid command pattern that could be passed to addCommand(). Any variables extracted from the command will be returned from run(). 

###run()

This method is what starts the command line interface. As soon as this is called the prompt is generated through a call to the specified prompt function, and displayed. Then, the user entered command is checked against the command patterns. The command patterns are checked in the order they were defined and they stop being checked after the first match is found. It is valid to define more than one pattern that would match a given input, but this is only useful if each subsequent pattern matches commands that none of the previous patterns match. 
