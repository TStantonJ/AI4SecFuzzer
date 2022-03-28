import collections

import pytest

from serialization import marshal
from deserialization import unmarshal
from exceptions import SerializationError, DeserializationError

ValidTestCase = collections.namedtuple('ValidTestCase', 'py_version nosj_version')

CORRECT_TEST_CASES = [
        ValidTestCase({}, '{}'),
        ValidTestCase({'a': 1}, '{a:i1}'),
        ValidTestCase({'a': -123}, '{a:i-123}'),
        ValidTestCase({'a': 'abcd'}, '{a:abcds}'),
        ValidTestCase({'a': 'abcds'}, '{a:abcdss}'),
        ValidTestCase({'a': 'ab cd'}, '{a:ab cds}'),
        ValidTestCase({'a': 'ab<cd>ef'}, '{a:ab<cd>efs}'),
        ValidTestCase({'a': 'ab,cd'}, '{a:ab%2Ccd}'),
        ValidTestCase({'a': 'ab\x00ef'}, '{a:ab%00ef}'),
        ValidTestCase({'a': 1, 'b': 'c'}, '{a:i1,b:cs}'),
        ValidTestCase({'a':{'b':{'c':1}}}, '{a:{b:{c:i1}}}'),
        ValidTestCase({'a':{'b': 1}, 'c': {'d': 2}}, '{a:{b:i1},c:{d:i2}}')
        ]

@pytest.mark.parametrize('tc', CORRECT_TEST_CASES)
def test_serialization_ok(tc):
    got = marshal(tc.py_version)
    assert(got == tc.nosj_version)

@pytest.mark.parametrize('tc', CORRECT_TEST_CASES)
def test_deserialization_ok(tc):
    got = unmarshal(tc.nosj_version)
    assert(got == tc.py_version)

@pytest.mark.parametrize('arg', [
        None,
        12345,
        {'a':2.3},
])
def test_serialization_error(arg):
    with pytest.raises(SerializationError):
        marshal(arg)

@pytest.mark.parametrize('arg', [
        '',
        '[]',
        '{',
        '{aaaa}',
])
def test_deserialization_error(arg):
    with pytest.raises(DeserializationError):
        unmarshal(arg)
