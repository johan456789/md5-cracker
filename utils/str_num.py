from utils.constants import PASSWORD_LEN, SIZE_OF_ALPHABET


def n_to_nums(n, b=SIZE_OF_ALPHABET):
    """Convert a positive number n to its digit representation in base b."""
    digits = []
    while n > 0:
        digits.append(n % b)
        n = n // b
    # pad to PASSWORD_LEN
    while len(digits) < PASSWORD_LEN:
        digits.append(0)
    digits.reverse()
    return digits


def str2nums(s):
    nums = []
    for c in s:
        if c.islower():  # 0-25 is a-z
            nums.append(ord(c) - ord('a'))
        else:  # 26-51 is A-Z
            nums.append(ord(c) + 26 - ord('A'))
    return nums


def nums2str(nums):
    str_builder = []
    for n in nums:
        if n < 26:  # 0-25 is a-z
            str_builder.append(chr(n + ord('a')))
        else:  # 26-51 is A-Z
            str_builder.append(chr(n - 26 + ord('A')))
    return ''.join(str_builder)


# A-Z: 65-90, a-z: 97-122
def str_generator(start_s, end_s):
    # assuming start_s < end_s and are valid strings
    start_nums, end_nums = str2nums(start_s), str2nums(end_s)
    nums = start_nums
    while nums <= end_nums:
        yield nums2str(nums)

        # increment by 1
        i = len(nums) - 1
        while i >= 0:
            nums[i] = nums[i] + 1
            if nums[i] < SIZE_OF_ALPHABET:
                break
            nums[i] = 0
            i -= 1
        if i < 0:
            return


def str_count(start_s, end_s):
    """
    Returns the number of strings between start_s and end_s (inclusive).
    """
    count = 1
    start_nums, end_nums = str2nums(start_s), str2nums(end_s)
    for i in range(len(start_nums)):
        count += (end_nums[i] - start_nums[i]) * SIZE_OF_ALPHABET ** (len(start_nums) - i - 1)
    return count
