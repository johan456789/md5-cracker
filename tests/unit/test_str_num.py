import os
from string import ascii_letters
from utils.str_num import n_to_nums, str2nums, nums2str, str_count, str_generator


def test_n_to_nums():
    PASSWORD_LEN = int(os.environ.get('PASSWORD_LEN'))  # type: ignore
    assert n_to_nums(0, b=2) == [0] * PASSWORD_LEN
    n, nums_wo_padding = 3, [1, 1]
    expected = [0] * (PASSWORD_LEN - len(nums_wo_padding)) + nums_wo_padding
    assert n_to_nums(n, b=2) == expected
    n, nums_wo_padding = 16, [1, 0, 0, 0, 0]
    expected = [0] * (PASSWORD_LEN - len(nums_wo_padding)) + nums_wo_padding
    assert n_to_nums(n, b=2) == expected


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
    expected = ['a' + c for c in list(ascii_letters)]
    assert list(str_generator('aa', 'aZ')) == expected


def test_str_count():
    assert str_count('a', 'a') == 1
    assert str_count('a', 'b') == 2
    assert str_count('a', 'z') == 26
    assert str_count('A', 'Z') == 26
    assert str_count('X', 'Z') == 3
    assert str_count('a', 'Z') == 52
    assert str_count('ab', 'ab') == 1
    assert str_count('ab', 'ac') == 2
    assert str_count('aa', 'ba') == 53
    assert str_count('aa', 'ZZ') == 52 * 52
    assert str_count('aa', 'Za') == str_count('aa', 'ZZ') - str_count('Zb', 'ZZ')
    assert str_count('abc', 'Zbc') == str_count('abc', 'ZZZ') - str_count('Zbd', 'ZZZ')
