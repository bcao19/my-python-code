'''
Author       : caobin
Date         : 2022-08-15 09:36:43
LastEditors  : caobin
LastEditTime : 2022-08-15 12:49:10
FilePath     : \undefinedd:\bcao19\my-python-code\pytorch\mybenchmark.py
'''
import torch
from torch.utils import benchmark

typ = torch.float16

n = 1024 * 16

a = torch.randn(n, n).type(typ).cuda()

b = torch.randn(n, n).type(typ).cuda()

t = benchmark.Timer(stmt='a @ b', globals={'a':a, 'b':b})


x = t.timeit(50)

ans = 2*n**3 / x.median / 1e12
print(ans)