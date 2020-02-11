#%%
from utils import *
from functools import reduce
#%%
# At some point I will do multinomial iid 
def typical_element_prob(p, N):
    bid = binary_iid([1, 0], bern(p), N)
    prod = reduce(lambda x, y: x * y, map(lambda x: pow(x, N * x), bid.probs))
    return prod, bid.entropy(bid.outcomes)
p = 0.1
N = 100
tsp = []
etsp = []
dist = list(range(N))
diff = []
for n in dist:
    tep, h = typical_element_prob(p, n)
    etep = -n * h
    d = abs((1/n)*lg(1/tep) - h) if n != 0 else 0
    tsp.append(tep)
    etsp.append(pow(2, etep))
    diff.append(d)
plt.plot(dist, tsp, label="typical element prob")
plt.plot(dist, etsp, label="estimated tep")
plt.legend()
# %%
# uniform convergence? 
plt.plot(dist, diff)

# %%
