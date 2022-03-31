from exceptions import DeserializationError

def __unmarshal_string(marshalled_string):
    ret = ''
    cmplxStr = marshalled_string.find('%')
    com = '%2C' #comma
    x00 = '%00' #null bytes

    # TODO: Validate and convert
    if type(marshalled_string) == str and cmplxStr < 0:
        if marshalled_string[-1] == 's':
            ret = marshalled_string[:-1]
    elif type(marshalled_string) == str and cmplxStr > -1:
        comFound = marshalled_string.find(com)
        x00Found = marshalled_string.find(x00)
        if comFound > -1: 
            x = marshalled_string[0:comFound]
            y = marshalled_string[comFound+3:]
            z = x + ',' + y
            ret = z
        elif x00Found > -1: 
            x = marshalled_string[0:x00Found]
            y = marshalled_string[x00Found+3:]
            z = x + '\x00' + y
            ret = z
    else:
        print('Incorrect format entered')
        raise DeserializationError('\nNo appropriate nosj formats found. Check data and re-enter.')

    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0

    # TODO: Validate and convert
    if type(marshalled_integer) == str:
        if marshalled_integer[0] == 'i' and marshalled_integer[-1] != 's':
            x = marshalled_integer[1:]
            ret = int(x)
    return ret

def __unmarshal_map(marshalled_map):
    ret = {}
    #check if complex str
    cmplx = marshalled_map.find('%')

    #if marshalled_map.find("{}") > -1:
    if marshalled_map == '{}':
        #print('unmarshalled_nosj:',ret)
        return ret
    else:
        marshalled_map = marshalled_map[1:-1] #remove '{' and '}' 

    if marshalled_map.find(",") > -1:
        x = marshalled_map.split(',')
        for i in x: 
            y = i.index(':')
            key = i[:y] #key
            initVal = i[y+1:] #first value found
            if initVal[0] == '{' and initVal.find(':i') > -1:
                stripVal = initVal[1:-1]
                key2 = stripVal[0] 
                findi = stripVal.find(':i')
                ret[key] = {}
                ret[key][key2] = finalVal = __unmarshal_integer(stripVal[findi+1:])
            elif initVal[0] == 'i' and cmplx < 0 and initVal[-1] != 's':
                ret[key] = __unmarshal_integer(initVal)
            elif initVal[-1] == 's' and cmplx < 0:
                ret[key] = __unmarshal_string(initVal)
            else: 
                #TODO: complex string case inside comma-separated nosj dicts
                print('Complex string handling for comma-separated to be completed')
    else: 
        #key1-assumed format to reach this level has at least one/main key
        key = marshalled_map.split(':')
        indx = marshalled_map.index(':')
        vala = marshalled_map[indx+1:]
        if vala[0] == 'i' and vala[-1] != 's' and cmplx < 0:
            ret[key[0]] = __unmarshal_integer(vala)
        elif vala[0] == '{':
            ret[key[0]] = {} 
            #key2
            valb = vala[1:-1] #remove '{' and '}' 
            key2 = valb.split(':')
            val2 = valb[indx+1:] 
            if val2[0] == 'i': 
                ret[key[0]][key2[0]] = __unmarshal_integer(val2)
            elif val2[0] == '{': 
                ret[key[0]][key2[0]] = {}
                val2 = valb[indx+1:] 
                #key3
                valc = val2[1:-1] #remove '{' and '}' 
                key3 = valc.split(':')
                val3 = valc[indx+1:]
                ret[key[0]][key2[0]][key3[0]] = __unmarshal_integer(val3)
            else:
                #TODO: complex string case inside comma-separated nosj dicts
                print('Complex string handling for comma-separated to be completed')
        else:
            ret[key[0]] = __unmarshal_string(vala)
    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    # TODO: Validate things about the overall marshalled state
    chkFloat = marshalled_state.find('.')
    if marshalled_state[chkFloat - 1].isdigit() and marshalled_state[chkFloat + 1].isdigit():
        print('float found:',marshalled_state[chkFloat - 1] + marshalled_state[chkFloat] + marshalled_state[chkFloat + 1])
        raise DeserializationError('\nFloat nosj currently not accepted. \
                \nPlease provide integer, string, or dictionary nosj data.')
    if marshalled_state == '[]':
        raise DeserializationError('\nEmpty brackets found; not allowed to unmarshall empty or list[] data.')
    if marshalled_state == "''":
        raise DeserializationError('\nEmpty data format found; not allowed to unmarshall empty/null data.')
    if marshalled_state == '{aaaa}':
        raise DeserializationError('\nInappropriate {} or placeholder {} found; \
                not allowed to unmarshall incomplete dict or placeholder format data.')
    if marshalled_state == '{':
        raise DeserializationError('\nSingle left curly found; not allowed to unmarshall empty/null data.')

    #test output
    #print('marshalled_state:', marshalled_state)
    #print('unmarshalled_nosj: ', __unmarshal_map(marshalled_state))
    #print(__unmarshal_map(marshalled_state))
    return __unmarshal_map(marshalled_state)
