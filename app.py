from flask import Flask, render_template, request
import string
from hashlib import md5

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crack')
def crack():
    md5 = request.args.get('md5')
    # hash = hashlib.md5('123'.encode()).hexdigest()

    return render_template('crack.html', md5=md5)

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
            if nums[i] < 52:
                break
            nums[i] %= 52
            i -= 1
        if i < 0:
            return
