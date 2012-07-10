from __future__ import print_function
#from __future__ import division		#division is not actually used

class cli(object):
	def __init__(self):
		self.__prompt = lambda : '> '
		self.__noMatch = lambda x : print('Invalid command')
		self.__exit = ['exit','quit']
		self.__commands = []
	
	#The prompt should be a function that returns a string
	def setPrompt(self,prompt):
		if not hasattr(prompt, '__call__'):
			error('prompt should be a function')
		self.__prompt = prompt
	
	#The no match action should be a function, usually that
	#prints an applicable error message
	#if the no match function returns True, the run loop
	#will exit. if the no match function returns False or
	#None, the run loop will continue
	def setNoMatch(self,action):
		if not hasattr(prompt, '__call__'):
			error('no match action should be a function')
		self.__noMatch = action
	
	#a list of patterns to exit on
	#using the same format as the command patterns
	def setExit(self,exitList):
		newList = []
		for p in exitList:
			tmp = p.split()
			if not self._isValidPattern(tmp):
				error('invalid pattern in exitList')
			newList.append(tmp)
		self.__exit = newList
	
	def addCommand(self,command,function):
		commands = command.split()
		if not self._isValidPattern(commands):
			error('invalid command pattern \'' + command + '\'')
		self.__commands.append((commands,function))
	
	#determine if a given command matches a pattern
	#return a dictionary of all the variable values if it does match
	#return False if it does not match
	#pattern and command should be passed as lists of strings
	def _matchCommand(self,pattern,command):
		if not self._isValidPattern(pattern):
			error('invalid pattern')
		if len(pattern) != len(command):
			return False
		vars = dict()
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
	def _isValidPattern(self,pattern):
		vars = ['i','f','s']
		for id in pattern:
			if len(id) < 1:
				return False
			if id[0] == '%':
				if len(id) < 3:
					return False
				if not id[1] in vars:
					return False
		return True
	
	#run the prompt loop
	#return the value of the exit command variables in a dictionary
	def run(self):
		while True:
			#display prompt
			userCommand = raw_input(self.__prompt()).split()
			
			#check if the command is an exit command
			for p in self.__exit:
				vars = self._matchCommand(p,userCommand)
				if vars != False:
					return vars
			
			#check if the command is a normal command
			for pattern,function in self.__commands:
				vars = self._matchCommand(pattern,userCommand)
				if vars != False:
					function(userCommand,vars)
					break
			else: #i guess it isn't, call the no match function
				self.__noMatch(userCommand)
	