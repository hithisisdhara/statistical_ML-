#%%
from itertools import accumulate
from collections import Counter
import random, math
def lg(num):
    return math.log2(num)
class ensamble:
    def __init__(self, symbols, probs):
        assert len(set(symbols)) == len(symbols) == len(probs)
        assert all(x!=0 for x in probs)
        assert sum (probs) == 1
        self.outcomes = symbols
        self.probs = probs 
        self.prefix_sum = [0]+list(accumulate(self.probs))
        self.symb_prob = {symbols[i]:probs[i] for i in range(len(probs))}

    def toss(self):
        return random.random()

    def get_prob(self,sym):
        if not isinstance(sym, list):
            assert sym in self.outcomes
            return self.symb_prob[sym]
        else:
            sum = 0 
            for s in sym:
                assert s in self.outcomes
                sum += self.symb_prob[s]
            return sum
    def generate_symbol(self):
        t = self.toss()
        for i in range(1,len(self.prefix_sum)):
            if self.prefix_sum[i] > t:
                return self.outcomes[i-1]

    def info_content(self,sym):
            return 1/lg(self.symb_prob[sym])

    def entropy(self, sym):
        if not isinstance(sym,list):
            return self.symb_prob[sym]*self.info_content(sym)
        else:
            sum = 0 
            for s in sym:
                assert s in self.outcomes
                sum += self.entropy(s)
            return sum
    def raw_bit_content(self,sym):
        assert all([s in self.outcomes for s in sym])
        return lg(len(sym))
    
#%%
class iid(ensamble):
    def __init__(self,symbols, probs, N):
        super().__init__(symbols, probs)
        self.N = N 
        self.numsym = len(self.outcomes)
        self.total = pow(self.numsym, N)

    def prob_of_string(self, string):
        string = Counter(string)
        prob = 1 
        for k,v in string.items():
            assert k in self.outcomes
            prob *= self.symb_prob[k]
        return prob
    def chk_dict(self, sym_count:dict):
        assert all([s in self.outcomes for s in sym_count.keys()])
        assert len(sym_count) == self.numsym - 1 
        assert sum(sym_count.values()) < self.N

    def num_strings(self, sym_count:dict):
        self.chk_dict(sym_count)
        not_in = list(set(self.outcomes) - set(list(sym_count.keys())))
        sym_count[not_in]= self.N - sum(sym_count.values())
        
