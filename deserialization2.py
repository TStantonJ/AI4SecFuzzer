from exceptions import DeserializationError
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

def __isprintable(st):
    #is it a ASCII printable string
    cnt = 0
    while cnt < len(st):
        if __isprintablech(st[cnt]) ==  False:
          return False
        cnt += 1
    return True

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

    #check if the chars are part of alpha numeric and the valid chars above
    cnt=0
    while cnt < len(key):
        if key[cnt] not in valid_chars:
            if not __isalnum(key[cnt]):
                flag=False
        cnt += 1

    return flag

def __isvalid_hex(hex):
    valid_chars = "abcdefABCDEF"
    cnt=0
    flag = True

    #Check for 2 char , and see if they are digits or hex char above
    if len(hex) != 2:
        return False
    while cnt < len(hex):
        if hex[cnt] not in valid_chars:
            if not hex[cnt].isdigit():
                flag=False
                break
        cnt += 1

    if flag:
      #convert to int and check if the hex is between 0-255 (hex beyond ascii range not expected)
      conv = int(hex, 16)
      if conv >= 0 and  conv <= 255:
        flag = True
      else:
        flag = False

    return flag

def __isvalid_encode(enc_str):
    cnt=0
    flag = True

    #Validating if its encoded and is valid i.e. %xx and xx is a valid hex

    #if no % return False
    if enc_str.find('%') ==  -1:
        return False

    while cnt < len(enc_str):
        if enc_str[cnt] == '%':
            #Check if we have 2 characters after % to process
            if len(enc_str) > cnt+2:
                flag = __isvalid_hex(enc_str[cnt+1:cnt+3])
                if flag == False:
                    return False
            else:
                return False
        cnt += 1
    return True


def __process_complex(marshalled_string):
    ret = ''
    tmp_str = marshalled_string
    
    #Validate if its well formed encode if so use the urllib 
    if (__isvalid_encode(tmp_str)):
        return urllib.parse.unquote(tmp_str)
    else:
        raise DeserializationError("Invalid % encoded string, when parsing ")


def __unmarshal_string(marshalled_string):
    ret = ''
    tmp_str = marshalled_string

    #Check for % and for s before processing
    if tmp_str.find('%') ==  -1 and tmp_str[len(tmp_str)-1] != 's':
            raise DeserializationError("Invalid string (doesn't end with 's' or a complex string without %, when processing ")

    #Validate for string rules. If complex call the process_complex method to process
    if __isprintable(tmp_str):
        if tmp_str.find(',') >=0 or tmp_str.find('{') >= 0 or tmp_str.find('}') >= 0:
            raise DeserializationError("Invalid char ({ or } or ,) found when processing ")
        if tmp_str.find('%') >= 0: 
            ret = __process_complex(tmp_str)
        else:
            ret = tmp_str[:len(tmp_str)-1]
    else:
        raise DeserializationError("Invalid char found. Can only be ASCII printable (except { } ,) or % encoded, when processing ")

    return ret


def __unmarshal_integer(marshalled_integer):
    ret = 0 
    negativeflag = False

    #Check if its not empty and see if there is i if so start process
    tmp_str = marshalled_integer.strip()
    if tmp_str == '':
        raise DeserializationError("Missing value when processing possible int")
    if tmp_str[0] != 'i':
        raise DeserializationError("Missing 'i' when processing for possible int: "+marshalled_integer)
    else:
        #integer if the rest of the char are integers (and - allowed for negative number) 
        #values with just i and i- are incomplete
        cnt = 1
        #Negative sign logic
        if len(tmp_str) >= 2:
           if tmp_str[1] == '-':
               #ret += '-'
               negativeflag = True
               if len(tmp_str) >= 3:
                   cnt = 2 
               else:
                   raise DeserializationError("Missing value while looking for possible integer(only 'i-' present)")
           else:
               cnt = 1
        else:
            raise DeserializationError("Missing value while looking for possible integer(only 'i' present)")
            
        numstr=''
        #process if its digit
        while cnt < len(tmp_str):
            if tmp_str[cnt].isdigit():
                numstr += tmp_str[cnt]
                cnt += 1;
            else:
                raise DeserializationError("Invalid number. (only 0-9 allowed apart from i and - at the beginning) when processing '"+marshalled_integer+"'")
          
        #If negative sign seen before convert the number to its negative 
        if negativeflag:
          return int(numstr) * -1
        else:
          return int(numstr) 


def __capture_map(after_col):
    ret = ''

    #This method is to capture a map i.e.  all characters between { and } 

    #Remove the spaces around for easy processing
    tmp_str = after_col.strip()
    if tmp_str == '':
        raise DeserializationError("Missing/Empty value in the key:value ")

    #Check for {
    if tmp_str[0] != '{':
        raise DeserializationError("Missing { value while processing: "+after_col)

    brace_open = 0
    brace_close = 0

    #Get all values till you see a matching } if not raise exception
    cnt = 0
    #Lo
    while cnt < len(after_col):
        if after_col[cnt] == '{':
            brace_open += 1
        if after_col[cnt] == '}':
            brace_close += 1
        ret += after_col[cnt]
        if brace_close == brace_open and brace_open != 0:
            return ret
        cnt += 1

    raise DeserializationError("Missing close brace while processing: "+after_col+':'+after_col)


def __is_int(val):
    #*Quick* way to see if its int or string. Further validation is done in the actual marshal method for integer
    tmp_str = val.strip()
    if tmp_str == '':
        raise DeserializationError("Missing/Empty value in the key:value pair")
    if tmp_str.find('%') !=  -1:
        return False

    if tmp_str[0] == 'i' and tmp_str[len(tmp_str)-1] != 's':
        return True
    else:
        return False

def __unmarshal_map(marshalled_map):
    ret = {}

    # Remove spaces on both sides
    mstr = marshalled_map.strip() 
    if mstr == '':
        raise DeserializationError("Missing value in the key:value pair")

    # Look for {} at the end or error out if not present
    if mstr[0] != '{':
        raise DeserializationError("Missing begin '{' when processing: ")
    if mstr[len(mstr)-1] != '}':
        raise DeserializationError("Missing end '}' when processing: ")

    #remove the { and } braces before processing
    mstr = mstr[:len(mstr)-1][1:]

    cur_pos = 0

    #looking for key:val pairs

    first_item = True
    #Move through items (comma separated blocks)
    while cur_pos < len(mstr):
        #Find key 
        
        colpos = mstr.find(':',cur_pos)
        if colpos == -1:
            raise DeserializationError("Missing ':' when processing a key value pair in: ")

        if mstr[cur_pos] == ',':
            #During the second round
            cur_pos += 1
        key=mstr[cur_pos:colpos]
        if not __isvalid_key(key):
                raise DeserializationError("Invalid Key. (only alphanum (space) - _  +  . allowed) when processin ")

        cur_pos = colpos+1
    
        #Find Value and process
        #ie. get the characters after : and see if the first non space char is a { 
        #If the value is a map then capture the whole map and recurse

        #Getting  to end of value
        brace = False
        comma = False
        while (cur_pos < len(mstr)):
            if mstr[cur_pos] == '{':
                brace = True
                break
            if mstr[cur_pos] == ',':
                comma = True
                break
            else:
                break;

        #if brace (open { ) its a map, we need to capture the map and call this same method recursivly
        if brace:
            if cur_pos+1 < len(mstr):
                tmp_str = mstr[cur_pos:]
                tmp_map = __capture_map(tmp_str)
                cur_pos += len(tmp_map)
                unmarshalled_val = __unmarshal_map(tmp_map)
        else:
            #Not a map so it has to be String or Integer
            #get value till you see a , or } or end of string
            tmp_val = ''
            while (cur_pos < len(mstr)):
                if mstr[cur_pos] == '}':
                    break
                if mstr[cur_pos] == ',':
                    comma = True
                    break
                tmp_val += mstr[cur_pos]
                cur_pos += 1

            if __is_int(tmp_val):
                 unmarshalled_val = __unmarshal_integer(tmp_val)
            else:
                 unmarshalled_val = __unmarshal_string(tmp_val)

        if  len(ret) != 0 and key in ret:
            raise DeserializationError('Duplicate key found cannot add this key second time:')
        else:
            ret[key] = unmarshalled_val
        if comma:
           cur_pos += 1

           ret[key] = unmarshalled_val

    return ret 

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')

    return dict(__unmarshal_map(marshalled_state))
