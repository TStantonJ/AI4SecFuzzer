from exceptions import SerializationError
import urllib.parse

def __isprintablech(x):
    #is it an ASCII printable char
    symbols=" \"!#$%&'()*+,-./:;<=>?@[]^_`{|}~\\"
    if x[0] in symbols:
        return True
    if ord(x) >= ord('A') and ord(x) <= ord('Z'):
       return True
    if ord(x) >= ord('a') and ord(x) <= ord('z'):
       return True
    if ord(x) >= ord('0') and ord(x) <= ord('9'):
       return True
    return False

def __isalnum(c):
    # Check if the char is alpha num
    if ord(c) >= ord('A') and ord(c) <= ord('Z'):
       return True
    if ord(c) >= ord('a') and ord(c) <= ord('z'):
       return True
    if ord(c) >= ord('0') and ord(c) <= ord('9'):
       return True
    return False


def __isvalid_key(key):
    valid_chars = " -_+."
    flag=True

    cnt=0
    while cnt < len(key):
        if key[cnt] not in valid_chars:
            if not __isalnum(key[cnt]):
                flag=False
        cnt += 1

    return flag

def __marshal_string(py_string):
    spcl_char = "%,{}"
    ret = ''

    cnt=0
    # If special characters we %hex encode using urllib tools but the first 3 char are special so doing it manually 
    while cnt < len(py_string):
        if py_string[cnt] == "\"":
            ret += "%22"
        elif py_string[cnt] == "\'":
            ret += "%60"
        elif py_string[cnt] == "\\":
            ret += "%5C"
        elif __isprintablech(py_string[cnt]) and py_string[cnt] not in spcl_char:
            ret += py_string[cnt]
        else:
            ret += urllib.parse.quote(py_string[cnt])
        cnt += 1

    # If it has percent (encoded) 's' not need else we append 's'
    if ret.find('%') == -1:
        ret += 's'
    return ret

def __marshal_integer(py_int):
    ret = ''

    # Integer validation is done while filtering in map function so nothing much is needed here
    ret = 'i'+str(py_int)

    return ret

def __marshal_map(py_dict):
    ret = '{'

    #loop through key value pairs of the dictionary
    #if you find a dictionary in the value again call the same method recursively
    #and repeat the same process. If you find a string or int call the appropriate marshal methods
    #Note: technically you can only call python functions recursively 1000 times. 
    #You can consider alternative ideas if you expect dictionary nesting complexity above 1000

    val=''
    startflag = True
    for key, value in py_dict.items():
        #If second item or more we need to add a comma
        if startflag:
          startflag = False
        else:
          ret += ","
      
        #validation for key
        if __isvalid_key(key):
            ret += key+':'
        else:
            raise SerializationError("Invalid Key. (only alphanum (space) - _  +  . allowed)")

        #if dict recurse back.  
        if type(value) is dict:
          val = __marshal_map(value)
        elif type(value) is str:
          val = __marshal_string(value)
        elif type(value) is int:
          val = __marshal_integer(value)
        else:
            raise SerializationError("Invalid value type only Dict, String and Integer allowed")

        ret += val

    ret += '}'
    return ret

def marshal(unmarshalled_state):
    if unmarshalled_state is None:
        raise SerializationError('Input is None')
    if type(unmarshalled_state) != dict:
        raise SerializationError('Input is not a dict')

    return __marshal_map(unmarshalled_state)
