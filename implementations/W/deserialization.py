from exceptions import DeserializationError
import re
import ast


sign_bit = 0 #Used to tell if integer is positive or negative
def __unmarshal_string(marshalled_string):
	cplx_bit = 0
	if type(marshalled_string) == str: #Check if input is string
#==========================
# Trying something new
		lis = list(marshalled_string)
		found = marshalled_string.find('%')
		if found > -1:
			cplx_bit = 1
			spot = lis.index('%')
			val1 = lis[spot + 1]
			val2 = lis[spot + 2]
			val = int(str(val1) + str(val2), 16)
			enc = chr(val)
			marshalled_string = marshalled_string.replace(marshalled_string[spot], '')
			marshalled_string = marshalled_string.replace(marshalled_string[spot], '')
			marshalled_string = marshalled_string.replace(marshalled_string[spot], enc)
		else:
			pass

# Replace function on 's' in string to remove s from all non-commplex strings
		# Is 's' the last bit in a non-complex string?
		is_s = marshalled_string[len(marshalled_string) - 1]
		if is_s == 's' and cplx_bit == 0:
			marshalled_string = marshalled_string[:-1]
			
		else:
			pass
# Return marshalled_string		
		ret = marshalled_string
	
	else:
		raise DeserializationError('Error in __unmarshal_string')	
	
	return ret

def __unmarshal_integer(marshalled_integer):
	global sign_bit
	if marshalled_integer[0] == 'i':
		no_i = marshalled_integer[1:]
		if no_i.isnumeric():
			ret = no_i
		else:
			raise DeserializationError('Error in __unmarshal_integer')
	else:
		raise DeserializationError('Error in __unmarshal_integer_second')
# Positive or Negative number	
	print('sees integer')
	print(sign_bit)
	if sign_bit == 1: #The number was negative
		ret = '-' + ret
	else:
		pass # The number was positive
		
	return ret

def __unmarshal_map(marshalled_map):
	global sign_bit
####################################################################
#	if type(marshalled_map) is list:
#		val = marshalled_map
#		for i in val:
#			val += i
#		print(val)
#		for i in val:
#			if val.find(','):
#				val = re.split('[,]', val)
#				if len(val) 
#				new_val = val[0]
#				nxt_key = val[1]
#				if 
#	else:
#		pass
	spl = marshalled_map
	if len(spl) < 2:
		raise DeserializationError('Error: Not a valid input')
	else:
		pass
	spl = spl.replace(spl[0], "")
	if len(spl) < 2:
		raise DeserializationError('Error: Not a valid input')
	else:
		pass

# Remove the ending bracket to make unmarshalling easier
	if spl[len(spl) - 1] == '}':
		spl = spl.replace(spl[len(spl) - 1], "")
	else:
		pass
# RE statement seperates the key and valye based on the colon in between	
	spl = re.split('[:]', spl)

	v = 'not'
	ret = ''
	if len(spl) < 2:
		raise DeserializationError('Error: Not a valid input')
	else:
		pass
	key = spl[0]	
	value = spl[1]
################################RECURSION####################################
	if len(spl) > 2:
		print('Could not get Recursion to work for dictionary with more than 1 item')
#		value = spl[1:]
#		print(value)
#		ret += __unmarshal_map(value)
#		if v.isnumeric():
#			ret = '{\'' + key + '\': ' + ret + '}'
#		else:
#			ret = '{\'' + key + '\': \'' + ret + '\'}'
#		return ret
	else:
		pass
#############################################################################
	if type(value) == str:
		if value[0] == 'i':
			v = value[1:]
			if v[0] == '-':
				v = v[1:]
				sign_bit = 1 #Positive number = 0; Negative number = 1
			else:
				sign_bit = 0 #Positive number = 0; Negative number = 1

			if v.isnumeric():
				ret += __unmarshal_integer('i' + v)
			else:
				ret += __unmarshal_string(value)
		else:
			ret += __unmarshal_string(value)
	elif type(value) == dict:
		ret += __unmarshal_map(value)
	
	else:
		raise DeserializationError('Error in __unmarshal_map: Not type String')
	
#==============================================================
	# Format for return
	if v.isnumeric():
		ret = '{\'' + key + '\': ' + ret + '}'
	else:
		ret = '{\'' + key + '\': \'' + ret + '\'}'
#==============================================================
# Transform into dictionary
	ret = ast.literal_eval(ret)
	
	return ret

def unmarshal(marshalled_state):
	if marshalled_state == '{}':
		marshalled_state_unmarshalled = {}
	
	elif type(marshalled_state) is dict:
		raise DeserializationError('Input can not be a dictionary')
	else:
		if marshalled_state is None:
			raise DeserializationError('Input is None')
		if type(marshalled_state) != str:
			raise DeserializationError('Input is not a string')
#===============================================================
		if type(marshalled_state) == str:
			if marshalled_state.isspace() == True:
				raise DeserializationError('Input is not a string')
			else:
				marshalled_state_unmarshalled = __unmarshal_map(marshalled_state)
		
	return marshalled_state_unmarshalled
