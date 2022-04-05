from exceptions import DeserializationError
import urllib


def __unmarshal_string(marshalled_string):
	ret = ''
	# TODO: Validate and convert
	# BEGIN -> NC
	if type(marshalled_string) == str:
		if marshalled_string[len(marshalled_string) - 1] != 's':
			value = urllib.parse.unquote(marshalled_string)
			if value == marshalled_string or value is marshalled_string:
				raise DeserializationError('incorrect format')
			ret = value
		else:
			for x in range(0, len(marshalled_string) - 1):
				ret += marshalled_string[x]
			i = 0
			working = ''
			while i < len(marshalled_string) - 1:
				working += marshalled_string[i]
				i += 1
			workingString = urllib.parse.unquote(working)
			if workingString != ret and not (workingString is ret):
				ret = urllib.parse.unquote(marshalled_string)
	else:
		raise DeserializationError('Input is not a string')
	# END -> NC
	return ret

def __unmarshal_integer(marshalled_integer):
	ret = 0
	# TODO: Validate and convert
	# BEGIN -> NC
	if type(marshalled_integer) == str:
		if marshalled_integer[0] != 'i':
			raise DeserializationError('is not an integer string')
		working = ''
		for x in range(1, len(marshalled_integer)):
			working += marshalled_integer[x]
		ret = int(working)
	else:
		raise DeserializationError('was not a string')
	# END -> NC
	return ret

def testInt(inString):
	if type(inString) == str:
		if inString[0] != 'i':
			return False
		for x in range(1, len(inString)):
			if x == 1:
				if inString[x] != '-' and not isDigit(inString[x]):
					return False
			else:
				if not isDigit(inString[x]):
					return False
		return True
	else:
		raise DeserializationError('The input was not a string')

def isDigit(inString):
	if type(inString) == str:
		if inString == '0':
			return True
		elif inString == '1':
			return True
		elif inString == '2':
			return True
		elif inString == '3':
			return True
		elif inString == '4':
			return True
		elif inString == '5':
			return True
		elif inString == '6':
			return True
		elif inString == '7':
			return True
		elif inString == '8':
			return True
		elif inString == '9':
			return True
		else:
			return False
	else:
		raise DeserializationError('The input was not a string')

def __unmarshal_map(marshalled_map):
	ret = {}
	# TODO: Validate and parse using the data-type specific functions
	# BEGIN -> NC
	if type(marshalled_map) == str:
		colon = False
		openBracket = False
		closeBracket = False
		key = ''
		var = ''
		i = 0
		while i < len(marshalled_map):
			c = marshalled_map[i]
			if openBracket == False and colon == False and c == '{':
				openBracket = True
			elif openBracket == True and colon == False and c != ':':
				key += c
			elif openBracket == True and colon == False and c == ':':
				colon = True
			elif openBracket == True and colon == True and c != ',' and c != '}' and c != '{':
				var += c
			elif openBracket == True and colon == True and (c == ',' or c == '}') and c != '{':
				closeBracket = True
				if testInt(var) == False:
					value = __unmarshal_string(var)
				else:
					value = __unmarshal_integer(var)
				ret[key] = value
				var = ''
				key = ''
				colon = False
			elif openBracket == True and colon == True and c == '{':
				openBracketCount = 1
				closedBracketCount = 0
				working = '{'
				while(closedBracketCount != openBracketCount):
					i += 1
					if marshalled_map[i] == '}':
						closedBracketCount += 1
						working += marshalled_map[i]
					elif marshalled_map[i] == '{':
						openBracketCount += 1
						working += marshalled_map[i]
					else:
						working += marshalled_map[i]
				value = __unmarshal_map(working)
				ret[key] = value
				var = ''
				key = ''
				colon = False
				i += 1
			i += 1
	# END -> NC
	return ret

def unmarshal(marshalled_state):
	if marshalled_state is None:
		raise DeserializationError('Input is None')
	if type(marshalled_state) != str:
		raise DeserializationError('Input is not a string')
	# TODO: Validate things about the overall marshalled state
	# BEGIN -> NC
	working = trimLeading(marshalled_state)
	working = trimTrailing(working)
	checkBrackets(working)
	checkFirstAndLast(working)
	#checkForThingsBeforeBracket(working)
	checkForColon(working)
	# END -> NC
	return __unmarshal_map(working)

def trimLeading(marshalled_state):
	if type(marshalled_state) == str:
		working = ''
		i = 0
		found = False
		while i < len(marshalled_state):
			if marshalled_state[i] != ' ' and marshalled_state[i] != '\t' and marshalled_state[i] != '\n' and not found:
				working += marshalled_state[i]
				found = True
			elif found:
				working += marshalled_state[i]
			i += 1
		return working
	else:
		raise DeserializationError('The input is not a string')

def trimTrailing(pyString):
	if type(pyString) == str:
		i = 0
		maxValue = 0
		while i < len(pyString):
			if pyString[i] != ' ' and pyString[i] != '\t' and pyString != '\n':
				maxValue = i	
			i += 1
		j = 0
		working = ''
		while j < i:
			working += pyString[j]
			j += 1
		return working
	else:
		raise DeserializationError('The input is not a string')

def checkBrackets(pyString):
	if type(pyString) == str:
		if len(pyString) > 0:
			if pyString[0] != '{':
				raise DeserializationError('pyString[0] != {')
			if pyString[len(pyString) - 1] != '}':
				raise DeserializationError('pyString[len(pyString) - 1] != }')
		else:
			raise DeserializationError('len(input) == 0')
		if len(pyString) > 2:
			i = 1
			key = ''
			openBracket = 0
			closeBracket = 0
			colon = False
			colonCount = 0
			while i < len(pyString) - 1:
				if colon == False and pyString[i] != ':':
					key += pyString[i]
				elif colon == False and pyString[i] == ':':
					colon = True
					colonCount += 1
					if key == '':
						raise DeserializationError('Empty key')
				elif colon == True and pyString[i] == '{':
					openBracket += 1
				elif colon == True and pyString[i] == '}':
					closeBracket += 1
					if closeBracket > openBracket:
						raise DeserializationError('{ > }')
				elif colon == True and openBracket == closeBracket and pyString[i] == ',':
					key = ''
					colon = False
					
				i += 1
			if openBracket != closeBracket:
				raise DeserializationError('Brackets do not match')
			if colonCount <= 0:
				raise DeserializationError('There were no colons')
			  
	else:
		raise DeserializationError('the input is not a string')

def checkFirstAndLast(pyString):
	if type(pyString) == str:
		if len(pyString) > 0:
			if pyString[0] != '{':
				raise DeserializationError('pyString[0] != }')
			if pyString[len(pyString) - 1] != '}':
				raise DeserializationError('pyString[len(pyString) - 1] != }')
		else:
			raise DeserializationError('EMPTY STRING')
	else:
		raise DeserializationError('The input is not a string')

def checkForThingsBeforeBracket(pyString):
	if type(pyString) == str:
		openBracket = False
		i = 0
		while i < len(pyString) and not openBracket:
			if pyString[i] == '{':
				openBracket = True
			elif pyString[i] != ' ' and pyString[i] != '/n' and pyString[i] != '/t':
				raise DeserializationError('There was non white space before the opening brakcet')
			i += 1
	else:
		raise DeserializationError('The input is not a string')

def checkBracketsO(pyString):
	if type(pyString) == str:
		if len(pyString) > 0:
			if pyString[0] != '{':
				raise DeserailizationError('pyString[0] != {')
			if pyString[len(pyString) - 1] != '}':
				raise DeserailizationError('pyString[len(pyString) - 1] != }')
			i = 1
			key = ''
			colon = False
			comma = False
			openBracketCount = 1
			closeBracketCount = 1
			commaCount = 0
			colonCount = 0
			value = ''
			while i < len(pyString) - 1:
				if colon == False and pyString[i] != ':':
					key += pyString[i]
				elif colon == False and pyString[i] == ':':
					colon == True
					colon += 1
					if key == '':
						raise DeserializationError('Empty key value')
				elif colon == True and comma == False:
					if pyString[i] != ',':
						value += pyString[i]
					elif pyString[i] == ',' or i == len(pyString) - 2:
						y = 0 # come back here	
				i += 1
		else:
			raise DeserializationError('String was empty')
	else:
		raise DeserailizationError('Input is not a string')

def checkForColon(pyString):
	if type (pyString) == str:
		found = False
		openBracket = 0
		closeBracket = 0
		i = 0
		colon = False
		while i < len(pyString):
			if pyString[i] == '{':
				openBracket += 1
			elif pyString[i] == '}':
				closeBracket += 1
			elif pyString[i] == ':' and found:
				colon = True
			elif openBracket > 0 and pyString[i] != ':':
				found = True
			i += 1
		if not colon and found:
			raise DeserializationError('There is no colon')
	else:
		raise DeserializationError('The input is not a string')
