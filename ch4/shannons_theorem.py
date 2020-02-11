#%%
from utils import *
from itertools import accumulate
import statistics
import pandas as pd
import numpy as np
def get_H0_for_different_sequences(bid):
    over = list(range(bid.N + 1))
    size = []
    set_prob = []
    coeff_prob = []
    for k in over:
        d = {1: k}
        size.append(bid.num_strings(d))
        set_prob.append(bid.set_prob(d))
        coeff_prob.append(bid.prob_of_string(d))
    csize = accumulate(size)
    cdf = accumulate(set_prob)
    H0 = [round(lg(x)/bid.N, 4) for x in csize]
    delta = [round(1 - p,4) for p in cdf]
    return over, H0, delta, size, coeff_prob

def get_a_row(N, p):
    bid = binary_iid([1, 0], bern(p), N)
    entropy = bid.entropy(bid.outcomes)
    over, H0, delta, bin_coeff, str_prob = get_H0_for_different_sequences(bid)
    return N, H0, delta, entropy, bin_coeff, str_prob
#%%
Ns = [10, 210, 410, 610, 810, 1010]
p1 = 0.1
res = []
for N in Ns:
    print(N)
    res.append(get_a_row(N, p1))
#%%
df = pd.DataFrame(res, columns=["range", "H_delta", "delta", "entropy", "bin_coeff", "str_prob"], index = [str(n) for n in Ns])
#%%
dh_delta = df[["range", "H_delta", "delta", "entropy"]]
for a, b in dh_delta.iterrows():
    h = b['H_delta']
    d = b['delta']
    e = b['entropy']
    ax = list(range(int(a)+1))
    #plt.plot(ax, h, label=a)
    plt.plot(d, h, label=a)
plt.plot(d, [e]*len(d), label="System entropy")
plt.legend()
plt.xlabel("delta")
plt.ylabel("H_delta")
plt.show()
#%%

dh_conv = df[["range", "bin_coeff", "str_prob"]]
for a, b in dh_conv.iterrows():
    ax = list(range(int(a)+1))
    bc = b['bin_coeff']
    bcs = sum(bc)
    nbc = np.array(bc)/bcs
    sp = b['str_prob']
    conv = np.multiply(bc, sp)
    plt.plot(ax, nbc, label=a+" norm bc")
    #plt.plot(ax, sp, label=a + " p")
    plt.plot(ax, conv, label=a + " conv")
plt.legend()
plt.xlabel("N")

# %%
