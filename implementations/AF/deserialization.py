from exceptions import DeserializationError

def __unmarshal_string(marshalled_string):
    # TODO: Validate and convert
	if '%2C' in marshalled_string or '%00' in marshalled_string:
		ret = marshalled_string.replace('%2C', ',')
		ret = ret.replace('%00', '\x00')
	else:
		ret = marshalled_string[:-1]

	return ret

def __unmarshal_integer(marshalled_integer):
    # TODO: Validate and convert
	return int(marshalled_integer[1:])

def __dfs_dict(ret):
	for k in ret:
		value = ret[k]
		if type(value) == dict:
			__dfs_dict(ret[k])
		else:
			if '%2C' in value or '%00' in value:
				ret[k] = __unmarshal_string(value)
			elif value[-1] == 's':
				ret[k] = __unmarshal_string(value)
			elif value[0] == 'i':
				ret[k] = __unmarshal_integer(value)
			else:
				raise DeserializationError('Input is illegal')
	return ret

def __unmarshal_map(marshalled_map):
    # TODO: Validate and parse using the data-type specific functions
	i = 0
	is_word = False
	symbol = ['{', '}', ',', ':']	

	while i < len(marshalled_map):
		if not marshalled_map[i] in symbol:
			if not is_word:
				marshalled_map = marshalled_map[:i] + "'" + marshalled_map[i:]
				is_word = True

		else:
			if is_word:
				marshalled_map = marshalled_map[:i] + "'" + marshalled_map[i:]
				is_word = False

		i += 1

	ret = eval(marshalled_map)
	ret = __dfs_dict(ret)

	return ret

def unmarshal(marshalled_state):
	if marshalled_state is None:
		raise DeserializationError('Input is None')
	if type(marshalled_state) != str:
		raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state
	if not (marshalled_state.startswith('{') and marshalled_state.endswith('}')):
		raise DeserializationError('Input is illegal')

	if len(marshalled_state) > 2 and marshalled_state.find(':') == -1:
		raise DeserializationError('Input is illegal')
	return __unmarshal_map(marshalled_state)
