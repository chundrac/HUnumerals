from __future__ import division
from collections import defaultdict
import numpy as np
import random
from numpy import log,exp
from numpy.random import dirichlet,beta,multinomial,normal
#from scipy.special import gamma
import itertools



text ="""1 0	d a s
1 1	g y A r a
1 2	b A r a
1 3	t E r a
1 4	c au d a
1 5	p a n d r a
1 6	s o l a
1 7	s a t r a
1 8	a Th A r a
2 -1	u n n I s
2 0	b I s
2 1	i k k I s
2 2	b A I s
2 3	t E I s
2 4	c au b I s
2 5	p a c c I s
2 6	ch a b b I s
2 7	s a t t A I s
2 8	a T T A I s
3 -1	u n t I s
3 0	t I s
3 1	i k a t t I s
3 2	b a t t I s
3 3	t ain t I s
3 4	c aun t I s
3 5	p ain t I s
3 6	ch a t t I s
3 7	s ain t I s
3 8	a R t I s
4 -1	u n t A l I s
4 0	c A l I s
4 1	i k t A l I s
4 2	b a y A l I s
4 3	t ain t A l I s
4 4	c a v A l I s
4 5	p ain t A l I s
4 6	ch i y A l I s
4 7	s ain t A l I s
4 8	a R t A l I s
5 -1	u n c A s
5 0	p a c A s
5 1	i k y A v a n
5 2	b A v a n
5 3	t i r p a n
5 4	c au v a n
5 5	p a c p a n
5 6	ch a p p a n
5 7	s a t t A v a n
5 8	a T Th A v a n
6 -1	u n s a Th
6 0	s A Th
6 1	i k s a Th
6 2	b A s a Th
6 3	t i r s a Th
6 4	c aun s a Th
6 5	p ain s a Th
6 6	ch i y A s a Th
6 7	s a r s a Th
6 8	a R s a Th
7 -1	u n h a t t a r
7 0	s a t t a r
7 1	i k h a t t a r
7 2	b a h a t t a r
7 3	t i h a t t a r
7 4	c au h a t t a r
7 5	p a c h a t t a r
7 6	ch i h a t t a r
7 7	s a t h a t t a r
7 8	a Th h a t t a r
8 -1	u n y A s I
8 0	a s s I
8 1	i k y A s I
8 2	b a y A s I
8 3	t i r A s I
8 4	c au r A s I
8 5	p a c A s I
8 6	ch i y A s I
8 7	s a t t A s I
8 8	a T Th A s I
8 9	n a v A s I
9 0	n a v E
9 1	i k y A n v E
9 2	b A n v E
9 3	t i r A n v E
9 4	c au r A n v E
9 5	p a c A n v E
9 6	ch i y A n v E
9 7	s a t t A n v E
9 8	a T Th A n v E
9 9	n i n y A n v E"""



text = text.split('\n')
for i in range(len(text)):
    text[i]=text[i].split('\t')
    text[i][1]=text[i][1].split()


forms = []
for l in text:
    w = l[1]
    forms.append(tuple(w))

def genmu(n):
    mu = {}
    for w in forms:
        mu[w] = {}
        for i in range(n,len(w)-n+1):
            mu[w][i] = 1
        mu[w][0] = 1
    return mu


mu = genmu(2)


iters = 10000
chains = 3
posterior = defaultdict()



def genfeats2gram():
    feats = []
    feats_0 = defaultdict()
    feats_10 = defaultdict()
    for w in forms:
        feats_0[w] = defaultdict(list)
        feats_10[w] = defaultdict(list)
        for m in mu[w].keys():
            w_0,w_10=['#']+list(w[:m]),list(w[m:])+['#']
            for i in range(len(w_0)-1):
                feats_0[w][m].append(tuple(w_0[i:i+2]))
                feats.append(tuple(w_0[i:i+2]))
            for i in range(len(w_10)-1):
                feats_10[w][m].append(tuple(w_10[i:i+2]))
                feats.append(tuple(w_10[i:i+2]))
#    """segmentation for monomorphemic representation"""
    feats = list(sorted(set(feats)))
    return feats_0,feats_10,feats


def genfeats1gram():
    feats = []
    feats_0 = defaultdict()
    feats_10 = defaultdict()
    for w in forms:
        feats_0[w] = defaultdict(list)
        feats_10[w] = defaultdict(list)
        for m in mu[w].keys():
            w_0,w_10=['#']+list(w[:m]),list(w[m:])+['#']
            for i in range(1,len(w_0)):
                feats_0[w][m].append(w_0[i])
                feats.append(w_0[i])
            for i in range(len(w_10)-1):
                feats_10[w][m].append(w_10[i])
                feats.append(w_10[i])
#    """segmentation for monomorphemic representation"""
    feats = list(sorted(set(feats)))
    return feats_0,feats_10,feats


def genfeats12gram():
    feats = []
    feats_0 = defaultdict()
    feats_10 = defaultdict()
    for w in forms:
        feats_0[w] = defaultdict(list)
        feats_10[w] = defaultdict(list)
        for m in mu[w].keys():
            w_0,w_10=['#']+list(w[:m]),list(w[m:])+['#']
            for i in range(len(w_0)-1):
                feats_0[w][m].append(tuple(w_0[i:i+2]))
                feats.append(tuple(w_0[i:i+2]))
            for i in range(1,len(w_0)):
                feats_0[w][m].append(w_0[i])
                feats.append(w_0[i])
            for i in range(len(w_10)-1):
                feats_10[w][m].append(tuple(w_10[i:i+2]))
                feats.append(tuple(w_10[i:i+2]))
            for i in range(len(w_10)-1):
                feats_10[w][m].append(w_10[i])
                feats.append(w_10[i])
#    """segmentation for monomorphemic representation"""
    feats = list(sorted(set(feats)))
    return feats_0,feats_10,feats


feats_0,feats_10,feats=genfeats2gram()


omega = defaultdict()
omega[0] = defaultdict(list)
omega[10] = defaultdict(list)
for i in range(1,10):
    """priors for features associated with TENS{1,...,9}"""
    omega[10][i]=[.1]*len(feats)


for i in range(1,11):
    """priors for features associated with DIGITS{-1,1,...,9}"""
    omega[0][i]=[.1]*len(feats)



def infer(c):
    posterior[c] = defaultdict()
    for w in forms:
        posterior[c][w] = defaultdict(int)
    g = .1
    for t in range(iters):
        cache = []
        words = random.sample(forms,len(forms))
        for w in words:
            m_c = mu_curr[w]
            i_c = i_curr[w]
            j_c = j_curr[w]
            for f in feats_10[w][m_c]:
                omega[10][i_c][feats.index(f)] -= 1
            morphs_10.pop(morphs_10.index(w[m_c:]))
            for f in feats_0[w][m_c]:
                omega[0][j_c][feats.index(f)] -= 1
            if j_c != 0:
                morphs_0.pop(morphs_0.index(w[:m_c]))
            pis = {}
            for m in mu[w].keys():
                if m == 0:
                    for i in range(1,10):
#                      if (i,0) not in cache[-10:] or t > 10:
                        p = log(mu[w][m]) - log(len(set(morphs_10+morphs_0+[w])))
                        for f in set(feats_10[w][m]):
                            for k in range(1,feats_10[w][m].count(f)+1):
                                p += log(omega[10][i][feats.index(f)]+k-1)
                        for l in range(1,len(feats_10[w][m])+1):
                            p -= log(sum(omega[10][i])+l-1)
                        pis[(m,i,0)] = exp(p)**g
                else:
                    for i in range(1,10):
                        for j in range(1,11):
#                          if (i,j) not in cache[-10:] or t > 10:
                            p = log(mu[w][m]) - log(len(set(morphs_10+morphs_0+[w[m:],w[:m]])))
                            for f in set(feats_10[w][m]):
                                for k in range(1,feats_10[w][m].count(f)+1):
                                    p += log(omega[10][i][feats.index(f)]+k-1)
                            for l in range(1,len(feats_10[w][m])+1):
                                p -= log(sum(omega[10][i])+l-1)
                            for f in set(feats_0[w][m]):
                                for k in range(1,feats_0[w][m].count(f)+1):
                                    p += log(omega[0][j][feats.index(f)]+k-1)
                            for l in range(1,len(feats_0[w][m])+1):
                                p -= log(sum(omega[0][j])+l-1)
                            pis[(m,i,j)] = exp(p)**g
            Z = sum(pis.values())
            for k in pis.keys():
                pis[k] = pis[k]/Z
            z = list(multinomial(1,pis.values()))
            z = z.index(1)
            z = pis.keys()[z]
            m,i,j = z
            mu_curr[w] = m
            i_curr[w] = i
            j_curr[w] = j
            if t > iters/2 and t/10 == int(t/10):
                posterior[c][w][(m,i,j)] += 1
            for f in feats_10[w][m]:
                omega[10][i][feats.index(f)] += 1
            morphs_10.append(w[m:])
            if j != 0:
                for f in feats_0[w][m]:
                    omega[0][j][feats.index(f)] += 1
                morphs_0.append(w[:m])
            cache.append((i,j))
            print c,t,m,i,j,w
        if t < 5000 and t/500 == int(t/500):
            g += .1


for c in range(chains):
    morphs_0 = []
    morphs_10 = []
    mu_curr = {}
    i_curr = {}
    j_curr = {}
    words = random.sample(forms,len(forms))
    for w in words:
        m = random.sample(mu[w].keys(),1)[0]
        mu_curr[w] = m
        i = random.sample(range(1,10),1)[0]
        i_curr[w] = i
        for f in feats_10[w][m]:
            omega[10][i][feats.index(f)]+=1
        morphs_10.append(w[m:])
        if m == 0:
            j = 0
        else:
            j = random.sample(range(1,11),1)[0]
            for f in feats_0[w][m]:
                omega[0][j][feats.index(f)]+=1
            morphs_0.append(w[:m])
        j_curr[w] = j
    infer(c)


f = open('hindi11to99mu2bigramMDL1annealMAP.txt','w')
for c in posterior.keys():
    for w in posterior[c].keys():
        for k in sorted(posterior[c][w].keys(),key=lambda(x):posterior[c][w][x])[::-1]:
            print >>f, c,''.join(w),k[0],k[1],k[2],posterior[c][w][k]


f.close()

