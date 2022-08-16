


import torch
from torch.utils import benchmark

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