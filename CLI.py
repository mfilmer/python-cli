from __future__ import print_function
import re
#from __future__ import division        #division is not actually used

class cli(object):
    """Module to allow for easy implementation of a 
    command line driven program"""
    def __init__(self):
        """Set up default prompt, no match actions, and exit commands"""
        self.__prompt = lambda : '> '
        self.__noMatch = lambda x,y : print('Invalid command')
        self.__exit = map(re.compile,['^exit$','^quit$'])
        self.__commands = [([],lambda x,y:None)]

    #The prompt should be a function that returns a string
    def setPrompt(self,prompt):
        """Supply a function that returns a string. This function is called
        every time the prompt is to be displayed. The returned string will
        be the prompt. Normally the string should end in a space ie: '> '
        The default prompt function is:
        lambda : '> '"""
        if not hasattr(prompt, '__call__'):
            raise ValueError('prompt should be a function')
        self.__prompt = prompt

    #The no match action should be a function, usually that
    #prints an applicable error message
    #if the no match function returns True, the run loop
    #will exit. if the no match function returns False or
    #None, the run loop will continue
    def setNoMatch(self,function):
        """The no match function is the function called when a user enters a
        command that is not matched by any of the command patterns. By 
        default this is to display "Invalid command" and return the prompt.
        The no match function should take two parameters. These parameters
        are similar to those accepted by function passed to the addCommand()
        function. The first is the user entered command, the second is the
        cli object, not a dictionary."""
        if not hasattr(function, '__call__'):
            raise TypeError('no match function should be a function')
        self.__noMatch = function

    #a list of patterns to exit on
    #uses the same format as the command patterns
    def setExit(self,exitList):
        """Set up the list of commands that will cause the run loop to exit.
        exitList should be a list of strings where each string is a valid
        command pattern as would be provided in a call to addCommand(). Any
        values to be extracted from the exit command will be returned from 
        the call to run()"""
        self.__exit = [re.compile(p) for p in exitList]

    def addCommand(self,pattern,function):
        """Specify a command pattern and a function to call. The function 
        will be called when a command matches the command pattern. 
        The command pattern should be formatted according to python's regular
        expression rules"""
        
        self.__commands.append((re.compile(pattern),function))

    #determine if a given command matches a pattern
    #return a dictionary of all the variable values if it does match
    #return False if it does not match
    def __matchCommand(self,pattern,command):
        a = pattern.match(command)
        if a is not None:
            return a.groupdict()

    #run the prompt loop
    #return the value of the exit command variables in a dictionary
    def run(self):
        """Run the main loop. During this loop the prompt will be displayed
        and the program will wait for user entered commands. This function
        will return a dictionary containing values extracted from the exit
        command"""
        while True:
            #display prompt
            try:    #maybe expand this try block around the whole loop
                userCommand = raw_input(self.__prompt())
            except KeyboardInterrupt:   #if the user types ^C
                break
            except EOFError:    #sometimes this is the ^C exception
                break

            #check if the command is an exit command
            for pattern in self.__exit:
                vars = self.__matchCommand(pattern,userCommand)
                if vars is not None:
                    return (userCommand,vars)

            #check if the command is a normal command
            for pattern,function in self.__commands:
                vars = self.__matchCommand(pattern,userCommand)
                if vars is not None:
                    function(userCommand,vars)
                    break
            else: #i guess it isn't, call the no match function
                self.__noMatch(userCommand,self)
