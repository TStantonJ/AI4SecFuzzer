from exceptions import DeserializationError
from urllib.parse import unquote

def __check_string(marshalled_string):
    
    my_string = marshalled_string
    
    if my_string[len(my_string) - 1] != 's':
        return False
    
    my_substring = my_string[0:len(my_string) - 1]
    
    for i in my_substring:
    
        if ord(i) == 37 or ord(i) == 44 or ord(i) == 123 or ord(i) == 125:
            return False
        
        elif ord(i) >=32 and ord(i) <= 126:
            continue
        
        else:
            return False
    return True

def __unmarshal_string(marshalled_string):
    
    ret = str(marshalled_string[0:len(marshalled_string) - 1])
    return ret

def __unmarshal_complex_string(marshalled_string):
    return str(unquote(marshalled_string))

def __check_int(py_int):
    my_int = py_int
    negative = False
    
    if my_int[0] != 'i':
        return False
    
    number = my_int[1:len(my_int)]
    
    if ord(number[0]) == 45:
        negative = True
    
    if negative is True:
        number = number[1:len(number)]
    
    for i in number:
    
        if ord(i) >= 48 and ord(i) <= 57:
            continue
        
        else:
            return False
    
    return True


def __unmarshal_integer(marshalled_integer):
    
    ret = int(marshalled_integer[1:len(marshalled_integer)])
    return ret

def __check_key(py_str):
    my_key = py_str
    
    for i in my_key:
        
        if ord(i) >= 48 and ord(i) <= 57:
            continue
        
        elif ord(i) >= 65 and ord(i) <= 90:
            continue
        
        elif ord(i) >= 97 and ord(i) <= 122:
            continue
        
        elif ord(i) == 32 or ord(i) == 45 or ord(i) == 95 or ord(i) == 43 or ord(i) == 46:
            continue
        
        else:
            return False
    
    return True


def __unmarshal_map(marshalled_map):
    new_value = "" 
    notMap = False
    before_comma = ""
    after_comma = ""
    key = ""
    comma_substring = ""
    value = ""
    dict_value = ""
    dict_key = ""
    get_key = True
    key_found = False
    is_Map = False
    hasComma = True
    value_substring = ""
    substring = marshalled_map
    leftBracket = 0
    rightBracket = 0
    comma_substring = ""
    
    for i in substring:
        if i == ':':
            get_key = False
            key_found = True
        if get_key is True:
            key += i
        if key_found is True:
            value_substring = substring[len(key) + 1: len(substring)]
            key_found = False
            if __check_key(key) is False:
                raise DeserializationError("Key is not accepted")
    dict_key = key
    for i in value_substring:
        if value_substring[0] == '{':
            is_Map = True 
        if i == '{' and is_Map == True:
            leftBracket += 1
        if i == '}' and is_Map == True:
            rightBracket += 1
        if leftBracket == rightBracket and is_Map == True:
            value += i
            break
        value += i

    if value_substring[len(value):len(value_substring)] != 0:
        comma_substring = str(value_substring[len(value):len(value_substring)])

    if value[0] == '{' and value[len(value) - 1] == '}':
        dict_value = unmarshal(value)
    
    elif __check_int(value) == True:
        dict_value = int(__unmarshal_integer(value))
    
    elif __check_string(value) == True:
        dict_value = str(__unmarshal_string(value))
    
    elif value.count(',') > 0:
        for i in value:
            if i == ',':
                break
            new_value += i
        after_comma = value[len(new_value) + 1:len(value) - 1]
        print(after_comma)
        value = new_value
        if __check_int(value) == True:
            dict_value = int(__unmarshal_integer(value))
        elif __check_string(value) == True:
            dict_value = str(__unmarshal_string(value))
        else:
            dict_value = str(__unmarshal_complex_string(value))
 
    else:
        dict_value = str(__unmarshal_complex_string(value))
    
    my_dict = {dict_key: dict_value} 
    print(my_dict)
    if len(comma_substring) != 0:
        another_substring = comma_substring[1:len(comma_substring)]
        temp = __unmarshal_map(another_substring)
        ret = my_dict.update(temp)

    if len(after_comma) != 0:
        test = __unmarshal_map(after_comma)
        ret = my_dict.update(test)

    ret = my_dict
    return ret

def unmarshal(marshalled_state):
    marshalled = marshalled_state.strip()
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')
    
    if len(marshalled) == 0:
        raise DeserializationError('String length is zero')
    
    if marshalled[0] != '{' or marshalled[len(marshalled) - 1] != '}':
        raise DeserializationError('Input cannot be converted to dict')
    
    if ':' not in marshalled and marshalled != "{}":
        raise DeserializationError('Input cannot be converted to a dict')

    if marshalled.count('{') != marshalled.count('}'):
        raise DeserializationError("Input cannot be converted to a dict")
    if marshalled_state == "{}":
        return {}
    marshalled = marshalled[1:len(marshalled) - 1]
    return __unmarshal_map(marshalled)
