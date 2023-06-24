import string
from utils.str_num import n_to_nums, str2nums, nums2str, str_generator
from utils.constants import PASSWORD_LEN, SIZE_OF_ALPHABET

def test_n_to_nums():
    assert n_to_nums(0, b=2) == [0] * PASSWORD_LEN
    n, nums_wo_padding = 3, [1, 1]
    assert n_to_nums(n, b=2) == [0] * (PASSWORD_LEN - len(nums_wo_padding)) + nums_wo_padding
    n, nums_wo_padding = 16, [1, 0, 0, 0, 0]
    assert n_to_nums(n, b=2) == [0] * (PASSWORD_LEN - len(nums_wo_padding)) + nums_wo_padding

def test_str2nums():
    assert str2nums('') == []
    assert str2nums('a') == [0]
    assert str2nums('z') == [25]
    assert str2nums('A') == [26]
    assert str2nums('Z') == [51]
    assert str2nums('abcABC') == [0, 1, 2, 26, 27, 28]

def test_nums2str():
    assert nums2str([]) == ''
    assert nums2str([0]) == 'a'
    assert nums2str([25]) == 'z'
    assert nums2str([26]) == 'A'
    assert nums2str([51]) == 'Z'
    assert nums2str([0, 1, 2, 26, 27, 28]) == 'abcABC'

def test_str_generator():
    assert list(str_generator('a', 'a')) == ['a']
    assert list(str_generator('a', 'b')) == ['a', 'b']
    assert list(str_generator('a', 'c')) == ['a', 'b', 'c']
    assert list(str_generator('aa', 'aZ')) == ['a' + c for c in list(string.ascii_letters)]
