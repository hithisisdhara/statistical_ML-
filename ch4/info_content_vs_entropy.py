#%%
from utils import * 
import matplotlib.pyplot as plt 

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
plt.plot(p,l)
# %%
