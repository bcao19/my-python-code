'''
Author       : caobin
Date         : 2022-08-15 09:36:43
LastEditors  : caobin
LastEditTime : 2022-08-26 13:37:25
FilePath     : \my-python-code\pytorch\mybenchmark.py
'''



import torch
import inspect
from collections import defaultdict
import pandas as pd
from torch.utils import benchmark


print('Pytorch version\t:', torch.__version__)
print('CUDA version\t:', torch.version.cuda)
print('GPU\t\t:',torch.cuda.get_device_name())


typ = torch.float16

n = 1024 * 16

a = torch.randn(n, n).type(typ).cuda()
b = torch.randn(n, n).type(typ).cuda()

# a = torch.randn(n, n).type(typ)
# b = torch.randn(n, n).type(typ)

t = benchmark.Timer(stmt='a @ b', globals={'a':a, 'b':b})

x = t.timeit(50)

ans = 2*n**3 / x.median / 1e12
print(ans)