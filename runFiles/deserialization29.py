import re
import urllib.parse

from exceptions import DeserializationError


def __unmarshal_string(marshalled_string):
    ret = ''

    # TODO: Validate and convert
    if marshalled_string.__contains__("%") or marshalled_string.__contains__(",") \
            or marshalled_string.__contains__("{") or marshalled_string.__contains__("}") \
            or marshalled_string.__contains__("\x00"):
        ret = urllib.parse.unquote(marshalled_string)
    else:
        ret = marshalled_string[:len(marshalled_string) - 1]
    return ret


def __unmarshal_integer(marshalled_integer):
    ret = 0

    # TODO: Validate and convert
    toint = marshalled_integer[1:len(marshalled_integer)]
    ret = int(toint)
    return ret


def __unmarshal_map(marshalled_map):
    ret = {}

    # TODO: Validate and parse using the data-type specific functions
    if len(marshalled_map) == 2:
        return ret
    k1 = re.compile('[:]+')
    v1 = k1.search(marshalled_map)
    key = marshalled_map[1:v1.start()]
    __validate_key__(key)
    if marshalled_map.__contains__(','):
        p = re.compile(('[,]+'))
        m = p.search(marshalled_map)
        value1 = marshalled_map[v1.start() + 1:m.start()]
        value2 = '{' + marshalled_map[m.start() + 1: len(marshalled_map) - 1] + '}'
        if value1[0] == 'i' and not value1.__contains__('%') and not value1.__contains__(',') \
                and not value1[len(value1) - 1] == 's':
            ret[key] = __unmarshal_integer(value1)
        elif not value1.__contains__('{') or not value1.__contains__('}') \
                or not value1.__contains__(':'):
            ret[key] = __unmarshal_string(value1)
        else:
            ret[key] = __unmarshal_map(value1)
        while True:
            k1 = re.compile('[:]+')
            v1 = k1.search(value2)
            key = value2[1:v1.start()]
            __validate_key__(key)
            if value2.__contains__(','):
                p = re.compile('[,]+')
                m = p.search(value2)
                value1 = value2[v1.start() + 1:m.start()]
                value2 = '{' + value2[m.start() + 1: len(value2) - 1] + '}'
                if value1[0] == 'i' and not value1.__contains__('%') and not value1.__contains__(',') \
                        and not value1[len(value1) - 1] == 's':
                    ret[key] = __unmarshal_integer(value1)
                elif not value1.__contains__('{') or not value1.__contains__('}') or not value1.__contains__(':'):
                    ret[key] = __unmarshal_string(value1)
                else:
                    ret[key] = __unmarshal_map(value1)
            else:
                value1 = value2[v1.start() + 1:len(value2) - 1]
                if value1[0] == 'i' and not value1.__contains__('%') and not value1.__contains__(',') \
                        and not value1[len(value1) - 1] == 's':
                    ret[key] = __unmarshal_integer(value1)
                elif not value1.__contains__('{') or not value1.__contains__('}'):
                    ret[key] = __unmarshal_string(value1)
                else:
                    ret[key] = __unmarshal_map(value1)
                break

    else:
        value1 = marshalled_map[v1.start() + 1:len(marshalled_map) - 1]
        if value1[0] == 'i' and not value1.__contains__('%') and not value1.__contains__(',') \
                and not value1[len(value1) - 1] == 's':
            ret[key] = __unmarshal_integer(value1)
        elif not value1.__contains__('{') or not value1.__contains__('}'):
            ret[key] = __unmarshal_string(value1)
        else:
            ret[key] = __unmarshal_map(value1)
    return ret


def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')


    # TODO: Validate things about the overall marshalled state
    if not marshalled_state.__contains__('{') or not marshalled_state.__contains__('}'):
        raise DeserializationError('Input is not a marshalled map')
    if not marshalled_state.__contains__(':') and len(marshalled_state) > 2:
        raise DeserializationError('Input is not a marshalled map')
    return __unmarshal_map(marshalled_state)

def __validate_key__(key):
    pattern = r'[^\s\-_+.a-z0-9]'
    if re.search(pattern, key):
        raise DeserializationError('Input has invalid key')

