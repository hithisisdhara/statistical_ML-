#%%
from utils import * 
import matplotlib.pyplot as plt 
bern = lambda x:[x,1-x]
#bc= ensamble([1,0],bern(0.1))
#sum([biased_coin.generate_symbol() for _ in range(20)])
#bc.info_content(1), bc.entropy(1), bc.get_prob([1])
Hanglish = ensamble(list("abcdefgh"),[1/4,1/4,1/4,3/16, 1/64, 1/64, 1/64, 1/64])
# %%
os = list("abcdefgh")
l = []
p = []
for e in list("abcdefgh")[::-1]:
    if os:
        l.append(lg(len(os)))
        setp = Hanglish.get_prob(os)
        p.append(1-setp)
        os.remove(e)
plt.scatter(p,l)
a# %%
