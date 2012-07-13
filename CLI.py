from __future__ import print_function
#from __future__ import division        #division is not actually used

class cli(object):
    """Module to allow for easy implementation of a 
    command line driven program"""
    def __init__(self):
        """Set up default prompt, no match actions, and exit commands"""
        self.__prompt = lambda : '> '
        self.__noMatch = lambda x,y : print('Invalid command')
        self.__exit = [['exit'],['quit']]
        self.__commands = []
    
    #The prompt should be a function that returns a string
    def setPrompt(self,prompt):
        """Supply a function that returns a string. This function is called
        every time the prompt is to be displayed. The returned string will
        be the prompt. Normally the string should end in a space ie: '> '
        The default prompt function is:
        lambda : '> '"""
        if not hasattr(prompt, '__call__'):
            error('prompt should be a function')
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
            error('no match function should be a function')
        self.__noMatch = function
    
    #a list of patterns to exit on
    #uses the same format as the command patterns
    def setExit(self,exitList):
        """Set up the list of commands that will cause the run loop to exit.
        exitList should be a list of strings where each string is a valid
        command pattern as would be provided in a call to addCommand(). Any
        values to be extracted from the exit command will be returned from 
        the call to run()"""
        newList = []
        for p in exitList:
            tmp = p.split()
            if not self.__isValidPattern(tmp):
                error('invalid pattern in exitList')
            newList.append(tmp)
        self.__exit = newList
    
    def addCommand(self,pattern,function):
        """Specify a command pattern and a function to call. The function 
        will be called when a command matches the command pattern. 
        Extra whitespace between words is ignored in command patterns and in
        user entered commands. When specifying a command pattern there are
        three special identifiers that allow extra information to be extracted
        from the user entered command. The folowing table shows these 
        identifiers and the data type they will extract from the command.
        Identifier | Function
             %i    | An integer value
             %f    | A floating point value
             %s    | A string value
        Words may not start with '%' in the command pattern unless they are
        one of these special identifiers
        After the identifier, there is a mandatory name. The name is made up
        of all the characters after the identifier before the next space. 
        This name is the name that will be the keyword in the dictionary that
        is passed to its corresponding function if the pattern matches.
        Example:
            pattern = 'set temp %ftemp'
        These patterns will match the folowing strings and result in the
        dictionary that is shown:
            'set temp 5.9'    -> {'temp':5.9}
            'set temp 34'    -> {'temp':34}
        But these patterns will not match
            'set temp apple'
            'set temp 48.7 and also 7.6'
        The integer identifier will only match words that can be converted
        to integers using the int() function. Likewise, the float identifier
        will only match words that can be converted to floats using the
        float() function. As the user input is read as a string, the string
        identifier will match all words. 
        
        Patterns can be specified that overlap. The patterns will be tested
        in the order they are added. For example if the first pattern entered
        is:
            pattern = 'set temp %i'
        The second pattern can be
            pattern = 'set temp %f'
        Then a third pattern could be
            pattern = 'set temp %s'
        As the float identifier is more general than the int, and the string
        identifier is more general than the float.
        
        The functions that are specified in the addCommand funcion will be
        called when the user enters a command that matches the corresponding
        pattern. These functions should take exactly two arguments. The first
        is a string containing the command the user entered. The second
        parameter is a dictionary containing all of the values extracted
        from the user entered command. 
        For example, if the pattern is:
            pattern = 'set temp %ftemp and name %sname'
        and the user had entered
            command = 'set temp 57.3 and name Joe'
        The dictionary passed to the function would be:
            {'temp':57.3, 'name':'Joe'}
        There is also an additional field in these dictionaies containing the
        cli object. This allows functions to modify acceptable commands. This
        field is called 'cli' and therefore 'cli' is not a valid name for a
        user defined field. Attempting to do so will result in an error"""
        
        commands = pattern.split()
        if not self.__isValidPattern(commands):
            error('invalid command pattern \'' + pattern + '\'')
        self.__commands.append((commands,function))
    
    #determine if a given command matches a pattern
    #return a dictionary of all the variable values if it does match
    #return False if it does not match
    #pattern and command should be passed as lists of strings
    def __matchCommand(self,pattern,command):
        if not self.__isValidPattern(pattern):
            error('invalid pattern')
        if len(pattern) != len(command):
            return False
        vars = {'cli':self}
        for p,c in zip(pattern,command):
            if p[0] == '%':
                if p[1] == 's':
                    vars[p[2:]] = c
                elif p[1] == 'f':
                    try:
                        vars[p[2:]] = float(c)
                    except:
                        return False
                elif p[1] == 'i':
                    try:
                        vars[p[2:]] = int(c)
                    except:
                        return False
            elif p != c:
                return False
        return vars
    
    #verify that a given pattern string is valid
    #pattern string is passed as a list of strings
    def __isValidPattern(self,pattern):
        vars = ['i','f','s']
        for id in pattern:
            if len(id) < 1:
                return False
            if id[0] == '%':
                if len(id) < 3:
                    return False
                if not id[1] in vars:
                    return False
                if id[2:] == 'cli':
                    return False
        return True
    
    #run the prompt loop
    #return the value of the exit command variables in a dictionary
    def run(self):
        """Run the main loop. During this loop the prompt will be displayed
        and the program will wait for user entered commands. This function
        will return a dictionary containing values extracted from the exit
        command"""
        while True:
            #display prompt
            rawCommand = raw_input(self.__prompt())
            userCommand = rawCommand.split()
            
            #check if the command is an exit command
            for p in self.__exit:
                vars = self.__matchCommand(p,userCommand)
                if vars != False:
                    return (rawCommand,vars)
            
            #check if the command is a normal command
            for pattern,function in self.__commands:
                vars = self.__matchCommand(pattern,userCommand)
                if vars != False:
                    function(rawCommand,vars)
                    break
            else: #i guess it isn't, call the no match function
                self.__noMatch(rawCommand,self)
