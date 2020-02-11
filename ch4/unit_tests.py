#%%
from scipy.special import comb
from utils import *
#%%
bid = binary_iid([1, 0], bern(0.2), 10)
print(bid.num_strings({0: 2}))
print(bid.prob_of_string({0: 2}))
print(bid.set_prob({0: 2}))
#%%
bc= ensamble([1,0],bern(0.1))
print(sum([bc.generate_symbol() for _ in range(20)]))
print(bc.info_content(1), bc.entropy(1), bc.get_prob([1]))
for k in range(bid.N + 1):
    print(k, bid.num_strings({1: k}))

# %%
