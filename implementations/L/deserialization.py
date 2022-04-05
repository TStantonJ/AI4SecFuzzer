from exceptions import DeserializationError
import copy


def is_integer(string1):
    return any(char.isdigit() for char in string1)


def __unmarshal_string(marshalled_string):
    ret = ''

    if marshalled_string == float:
        raise DeserializationError('Input is not a string')

    marshalled_string = str(marshalled_string)

    if '%2C' in marshalled_string or '%7B' in marshalled_string or '%7D' in marshalled_string or '%25' in marshalled_string:
        marshalled_string = marshalled_string.replace('%2C',',')
        marshalled_string = marshalled_string.replace('%7B','{')
        marshalled_string = marshalled_string.replace('%7D','}')
        ret += marshalled_string.replace('%25','%')
    else:
        ret = marshalled_string.replace(marshalled_string[len(marshalled_string)-1],"")
    return ret

def __unmarshal_integer(marshalled_integer):
    ret = 0


    #marshalled_integer = str(marshalled_integer)


    lin = marshalled_integer.replace("i", "")
    ret = int(lin)

    return ret


def __unmarshal_map(marshalled_map):
    ret = {}
    temp = {}
    new = []
    count = 0
    num = 0


    if len(marshalled_map) < 2:
        raise DeserializationError('Input is Not a Dictionary')
    elif marshalled_map[0] != '{' and marshalled_map[len(marshalled_map) -1] != '}':
        raise DeserializationError('Input is Not a Dictionary')
    elif ':' not in marshalled_map:
        raise DeserializationError('Input is Not a Dictionary')

    for x in marshalled_map:
        if x == '{':
            count += 1

    if count <= 1:
        marshalled_map = marshalled_map.replace('{','')
        marshalled_map = marshalled_map.replace('}','')
        marshalled_map = marshalled_map.split(',')
        for x in marshalled_map:
            array = []
            array = x.split(':')
            if len(array) < 2:
                break
            if '%' in array[1]:
                ret[array[0]] = __unmarshal_string(array[1])
            elif is_integer(array[1]) == True:
                ret[array[0]] = __unmarshal_integer(array[1])
            else:
                ret[array[0]] = __unmarshal_string(array[1])
    else:
        marshalled_map = marshalled_map.split(',')
        for x in marshalled_map:
            x = x.replace('{','')
            x = x.replace('}','')
            for y in x:
                if y == ':':
                    num +=1
            new = x.split(':')
            if num == 1:
                if '%' in new[1]:
                    ret[new[0]] = __unmarshal_string(new[1])
                elif is_integer(new[1]) == True:
                    ret[new[0]] = __unmarshal_integer(new[1])
                else:
                    ret[new[0]] = __unmarshal_string(new[1])
            else:
                i = len(new) -1
                while i > 0:
                    if i == len(new) - 1:
                        if '%' in new[i]:
                            ret[new[i-1]] = __unmarshal_string(new[i])
                            temp = copy.deepcopy(ret)
                        elif is_integer(new[i]) == True:
                            ret[new[i-1]] = __unmarshal_integer(new[i])
                            temp = copy.deepcopy(ret)
                        else:
                            ret[new[i-1]] = __unmarshal_string(new[i])
                            temp = copy.deepcopy(ret)
                    else:
                        ret.clear()
                        ret[new[i-1]] = copy.deepcopy(temp)
                        temp = copy.deepcopy(ret)
                    i -= 1

    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')
    #if type(marshalled_state) != int:
       # raise DeserializationError('Input is not an integer')

    return __unmarshal_map(marshalled_state)