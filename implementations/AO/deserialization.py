from exceptions import DeserializationError
import urllib

def __unmarshal_string(marshalled_string):
    ret = marshalled_string

    if ret.__contains__( '%' ):
        ret = urllib.parse.unquote( ret ).decode( 'utf8' )

    elif ret[ -1 ].__eq__( 's' ):
        ret = ret[ 0, -1 ]
    
    else:
        raise DeserializationError( 'Not a valid String' )

    return ret

def __unmarshal_integer(marshalled_integer):
    ret = marshalled_integer
    if ret[ 0 ].__eq__( 'i' ):
        ret = ret[ 1, -1 ]
    else:
        raise DeserializationError( 'Not a valid Integer' )

    return ret

def __unmarshal_map(marshalled_map):
    ret = {}
    key = ""
    lastelementplace = 0
    bracketplace = 0

    for char in marshalled_map:
        if char.__eq__( ':' ):
            key = marshalled_map[ lastelementplace : marshalled_map.index(char) : 1] 
            lastelementplace = marshalled_map.index( char )
        if char.__eq__( '{' ):
            bracketplace = marshalled_map.index(char)
            lastelementplace = lastelementplace + 1
        if char.__eq__( '}' ): 
            __unmarshal_map( marshalled_map[ bracketplace : marshalled_map.index(char) : 1 ] ) 
            bracketplace = 0
        if char.__eq__( ',' ):
            if marshalled_map[ lastelementplace ].__eq__( 'i' ):
                ret [ key ] = __unmarshal_integer( marshalled_map[ lastelementplace : marshalled_map.index(char) : 1 ] )
            elif marshalled_map[ lastelementplace : marshalled_map.index(char) ].__contains__( '%' ) or marshalled_map[ marshalled_map.index(char) ].__eq__( 's' ):
                ret [ key ] = __unmarshal_string ( marshalled_map [ lastelementplace : marshalled_map.index(char) : 1] )
            else:
                raise DeserializationError( 'Invalid value!' )

    return ret

def unmarshal(marshalled_state):
    if marshalled_state is None:
        raise DeserializationError('Input is None')
    if type(marshalled_state) != str:
        raise DeserializationError('Input is not a string')
    if marshalled_state != False and marshalled_state.__contains__( '{' ) == False or marshalled_state.__contains__( '}' ) == False or marshalled_state.__contains__( ':' ) == False:
        raise DeserializationError('Input is not a valid input')
    return __unmarshal_map(marshalled_state)
