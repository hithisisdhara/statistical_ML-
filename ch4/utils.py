#%%
from itertools import accumulate
from collections import Counter
import random, math
from scipy.special import comb
import matplotlib.pyplot as plt

def lg(num):
    return math.log2(num)


def draw_dot_line(x, y , l1 = ""):
    plt.scatter(x, y)
    plt.plot(x, y, label=l1)



class ensamble:
    def __init__(self, symbols, probs):
        try: 
            assert len(set(symbols)) == len(symbols) == len(probs)
            assert all(x!=0 for x in probs)
            assert sum(probs) == 1
        except:
            print("check definition of prob dist")
            return 
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

    def info_content(self, sym):
            '''
            of a symbol
            '''
            return lg(1/self.symb_prob[sym])

    def entropy(self, sym):
        '''
        if list is given, gets the entropy of the symbols in the list
        else gets the entropy of the string symbol 
        '''
        if not isinstance(sym,list):
            return self.symb_prob[sym]*self.info_content(sym)
        else:
            sum = 0 
            for s in sym:
                assert s in self.outcomes
                sum += self.entropy(s)
            return sum
    def raw_bit_content(self, sym):
        '''
        of a set of symbols 
        '''
        try:
            assert all([s in self.outcomes for s in sym])
            return lg(len(sym))
        except:
            print("symbols not in ensamble")
            return 
    


def bern(x): return [x, 1-x]
class binary_iid(ensamble):
    '''
    given an ensamble X, gets the iid for N tosses X^N
    '''
    def __init__(self, symbols, probs, N):
        try:
            assert len(symbols) == 2
        except:
            print("only binary ensamble excepted")
            return
        super().__init__(symbols, probs)
        self.N = N 
        self.numsym = len(self.outcomes)
        self.total = pow(self.numsym, N)
        self.bin_coef_memo = {}

    def prob_of_string(self, string):
        '''
        Given an arbitrary long string (not necessarily N long), gives the probability 
        of this string when len(string) many tosses 
        '''
        if isinstance(string, str):
            string = Counter(string)
        self.fill_dict(string)
        assert len(string) == self.numsym
        prob = 1 
        for k,v in string.items():
            prob *= pow(self.symb_prob[k],v)
        return prob

    def chk_dict(self, sym_count:dict):
        assert all([s in self.outcomes for s in sym_count.keys()])
        assert len(sym_count) == self.numsym - 1 or len(sym_count) == self.numsym
        assert sum(sym_count.values()) <= self.N

    def fill_dict(self, sym_count: dict):
        try:
            self.chk_dict(sym_count)
        except:
            print("issues with symbols")
            return
        if len(sym_count) == self.numsym - 1:
            other = list(set(self.outcomes) - set(sym_count.keys()))[0]
            sym_count[other] = self.N - sum(sym_count.values())

    def num_strings(self, sym_count: dict):
        self.fill_dict(sym_count)
        first, second = sym_count.keys()
        if int(sym_count[first]) in self.bin_coef_memo:
            return self.bin_coef_memo[int(sym_count[first])]
        else:
            coef = comb(self.N, sym_count[first])
            self.bin_coef_memo[int(sym_count[first])] = coef
            self.bin_coef_memo[int(sym_count[second])] = coef
            return coef

    def set_prob(self, sym_count: dict):
        return self.num_strings(sym_count) * self.prob_of_string(sym_count)  # this s the binomial coeff*value
        


# %%
