'''
Author       : caobin
Date         : 2022-05-11 17:20:06
LastEditors  : caobin
LastEditTime : 2022-08-26 10:03:15
FilePath     : \my-python-code\test.py
'''
print('中午')

print('20230117')
good555



# a function that extract all number from a string
def extract_number(s):
    number = ''
    for i in s:
        if i.isdigit():
            number += i
    return number