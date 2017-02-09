#!usr/bin/env python

from __future__ import division
import sys
from collections import defaultdict
import itertools
import numpy as np
from numpy import log

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
    text[i][0]=text[i][0].split()
    text[i][1]=text[i][1].split()


forms = []
for l in text:
    w = l[1]
    forms.append(tuple(w))


formdict = {}
for f in forms:
    formdict[''.join(f)]=f


truedigits = defaultdict(list)
truetens = defaultdict(list)

for l in text:
    truedigits[l[0][1]].append(''.join(l[1]))
    truetens[l[0][0]].append(''.join(l[1]))


truedigits=truedigits.values()
truetens=truetens.values()


def fmeasure(c,k): #c = clustering; k = true classification
    D = sum([len(x) for x in c])
    P = {}
    R = {}
    F = {}
    for i in range(len(k)):
        for j in range(len(c)):
            n_ij = 0
            for w in k[i]:
                if w in c[j]:
                    n_ij += 1
            R[(i,j)] = n_ij/len(k[i])
            P[(i,j)] = n_ij/len(c[j])
            if (R[(i,j)]+P[(i,j)]) != 0:
                F[(i,j)] = 2 * (R[(i,j)]*P[(i,j)])/(R[(i,j)]+P[(i,j)])
            else:
                F[(i,j)] = 0
    f = 0
    for i in range(len(k)):
        ck = []
        for key in F.keys():
            if key[0] == i:
                ck.append(F[key])
        f += (len(k[i])/D)*max(ck)
    return f


def homogeneity(c,k):
    N = len(forms)
    a_ck = np.zeros([len(c),len(k)])
    for i in range(len(c)):
        for j in range(len(k)):
            for w in k[j]:
                if w in c[i]:
                    a_ck[(i,j)] += 1
    hck = 0
    for i in range(len(c)):
        for j in range(len(k)):
            if a_ck[(i,j)] != 0:
                hck -= (a_ck[(i,j)]/N)*log(a_ck[(i,j)]/sum(a_ck[:,j]))
            else:
                hck -= 0
    hc = 0
    for i in range(len(c)):
        hc -= (sum(a_ck[i,:])/N)*log(sum(a_ck[i,:])/N)
#    print hck,np.isfinite(hck),hc,np.isfinite(hc)
    if np.isfinite(hck) and hc != 0:
        return 1-(hck/hc)
    else:
        return 1


def homogeneities(c,k):
    N = len(forms)
    a_ck = np.zeros([len(c),len(k)])
    for i in range(len(c)):
        for j in range(len(k)):
            for w in k[j]:
                if w in c[i]:
                    a_ck[(i,j)] += 1
    hck = 0
    for i in range(len(c)):
        for j in range(len(k)):
            if a_ck[(i,j)] != 0:
                hck -= (a_ck[(i,j)]/N)*log(a_ck[(i,j)]/sum(a_ck[:,j]))
            else:
                hck -= 0
    hc = 0
    for i in range(len(c)):
        hc -= (sum(a_ck[i,:])/N)*log(sum(a_ck[i,:])/N)
#    print hck,np.isfinite(hck),hc,np.isfinite(hc)
    return hck,hc


def vmeasure(c,k):
    H = homogeneity(c,k)
    C = homogeneity(k,c)
#    print H,C
    return 2*H*C/(H+C)


def NVI(c,k):
    N = len(forms)
    a_ck = np.zeros([len(c),len(k)])
    for i in range(len(c)):
        for j in range(len(k)):
            for w in k[j]:
                if w in c[i]:
                    a_ck[(i,j)] += 1
    hck = 0
    for i in range(len(c)):
        for j in range(len(k)):
            if a_ck[(i,j)] != 0:
                hck -= (a_ck[(i,j)]/N)*log(a_ck[(i,j)]/sum(a_ck[:,j]))
            else:
                hck -= 0
    hkc = 0
    for j in range(len(k)):
        for i in range(len(c)):
            if a_ck[(i,j)] != 0:
                hkc -= (a_ck[(i,j)]/N)*log(a_ck[(i,j)]/sum(a_ck[i,:]))
            else:
                hkc -= 0
    hc = 0
    for i in range(len(c)):
        hc -= (sum(a_ck[i,:])/N)*log(sum(a_ck[i,:])/N)
    hk = 0
    for j in range(len(k)):
        hk -= (sum(a_ck[:,j])/N)*log(sum(a_ck[:,i])/N)
#    print hck,np.isfinite(hck),hc,np.isfinite(hc)
    if hc != 0:
        return (hkc+hck)/hc
    else:
        return hk


def NVI(c,k):
    hck,hc = homogeneities(c,k)
    hkc,hk = homogeneities(k,c)
    if hc != 0:
        return (hck+hkc)/hc
    else:
        return hk


texforms=['{\\IPA/d@s/}', '{\\IPA/gj{\\textscripta}r@/}', '{\\IPA/b{\\textscripta}r@/}', '{\\IPA/ter@/}', '{\\IPA/cOd@/}', '{\\IPA/p@ndr@/}', '{\\IPA/sol@/}', '{\\IPA/s@tr@/}', '{\\IPA/@\\:t\\textsuperscript{h}{\\textscripta}r@/}', '{\\IPA/Unnis/}', '{\\IPA/bis/}', '{\\IPA/Ikkis/}', '{\\IPA/b{\\textscripta}is/}', '{\\IPA/teis/}', '{\\IPA/cObis/}', '{\\IPA/p@ccis/}', '{\\IPA/c\\textsuperscript{h}@bbis/}', '{\\IPA/s@tt{\\textscripta}is/}', '{\\IPA/@\\:t\\:t{\\textscripta}is/}', '{\\IPA/Untis/}', '{\\IPA/tis/}', '{\\IPA/Ik@ttis/}', '{\\IPA/b@ttis/}', '{\\IPA/t\\~{\x07e}tis/}', '{\\IPA/c\\~Otis/}', '{\\IPA/p\\~{\x07e}tis/}', '{\\IPA/c\\textsuperscript{h}@ttis/}', '{\\IPA/s\\~{\x07e}tis/}', '{\\IPA/@\\:rtis/}', '{\\IPA/Unt{\\textscripta}lis/}', '{\\IPA/c{\\textscripta}lis/}', '{\\IPA/Ikt{\\textscripta}lis/}', '{\\IPA/b@j{\\textscripta}lis/}', '{\\IPA/t\\~{\x07e}t{\\textscripta}lis/}', '{\\IPA/c@V{\\textscripta}lis/}', '{\\IPA/p\\~{\x07e}t{\\textscripta}lis/}', '{\\IPA/c\\textsuperscript{h}Ij{\\textscripta}lis/}', '{\\IPA/s\\~{\x07e}t{\\textscripta}lis/}', '{\\IPA/@\\:rt{\\textscripta}lis/}', '{\\IPA/Unc{\\textscripta}s/}', '{\\IPA/p@c{\\textscripta}s/}', '{\\IPA/Ikj{\\textscripta}V@n/}', '{\\IPA/b{\\textscripta}V@n/}', '{\\IPA/tIrp@n/}', '{\\IPA/c@uV@n/}', '{\\IPA/p@cp@n/}', '{\\IPA/c\\textsuperscript{h}@pp@n/}', '{\\IPA/s@tt{\\textscripta}V@n/}', '{\\IPA/@\\:t\\:t\\textsuperscript{h}{\\textscripta}V@n/}', '{\\IPA/Uns@\\:t\\textsuperscript{h}/}', '{\\IPA/s{\\textscripta}\\:t\\textsuperscript{h}/}', '{\\IPA/Iks@\\:t\\textsuperscript{h}/}', '{\\IPA/b{\\textscripta}s@\\:t\\textsuperscript{h}/}', '{\\IPA/tIrs@\\:t\\textsuperscript{h}/}', '{\\IPA/c\\~Os@\\:t\\textsuperscript{h}/}', '{\\IPA/p\\~{\x07e}s@\\:t\\textsuperscript{h}/}', '{\\IPA/c\\textsuperscript{h}Ij{\\textscripta}s@\\:t\\textsuperscript{h}/}', '{\\IPA/s@rs@\\:t\\textsuperscript{h}/}', '{\\IPA/@\\:rs@\\:t\\textsuperscript{h}/}', '{\\IPA/Unh@tt@r/}', '{\\IPA/s@tt@r/}', '{\\IPA/Ikh@tt@r/}', '{\\IPA/b@h@tt@r/}', '{\\IPA/tIh@tt@r/}', '{\\IPA/cOh@tt@r/}', '{\\IPA/p@ch@tt@r/}', '{\\IPA/c\\textsuperscript{h}Ih@tt@r/}', '{\\IPA/s@th@tt@r/}', '{\\IPA/@\\:t\\textsuperscript{h}h@tt@r/}', '{\\IPA/Unj{\\textscripta}si/}', '{\\IPA/@ssi/}', '{\\IPA/Ikj{\\textscripta}si/}', '{\\IPA/b@j{\\textscripta}si/}', '{\\IPA/tIr{\\textscripta}si/}', '{\\IPA/cOr{\\textscripta}si/}', '{\\IPA/p@c{\\textscripta}si/}', '{\\IPA/c\\textsuperscript{h}Ij{\\textscripta}si/}', '{\\IPA/s@tt{\\textscripta}si/}', '{\\IPA/@\\:t\\:t\\textsuperscript{h}{\\textscripta}si/}', '{\\IPA/n@V{\\textscripta}si/}', '{\\IPA/n@Ve/}', '{\\IPA/Ikj{\\textscripta}nVe/}', '{\\IPA/b{\\textscripta}nVe/}', '{\\IPA/tIr{\\textscripta}nVe/}', '{\\IPA/cOr{\\textscripta}nVe/}', '{\\IPA/p@c{\\textscripta}nVe/}', '{\\IPA/c\\textsuperscript{h}Ij{\\textscripta}nVe/}', '{\\IPA/s@tt{\\textscripta}nVe/}', '{\\IPA/@\\:t\\:t\\textsuperscript{h}{\\textscripta}nVe/}', '{\\IPA/nInj{\\textscripta}nVe/}']



texdict = {}
for i in range(len(forms)):
    texdict[''.join(forms[i])]=texforms[i]



def tabulate(fn):
  tens = defaultdict(list)
  digits = defaultdict(list)
  for c in ['0','1','2']:
    m = []
    for l in open(fn,'r'):
        m.append(l.split())
    t = defaultdict()
    d = defaultdict()
    for l in m:
        t[l[1]] = defaultdict(int)
        d[l[1]] = defaultdict(int)
    for l in m:
        if l[0]==c:
            t[l[1]][l[3]] = int(l[-1])
            d[l[1]][l[4]] = int(l[-1])
    tc = defaultdict(list)
    dc = defaultdict(list)
    for k in t.keys():
        z=max(t[k].values())
        y=t[k].values().index(z)
        x=t[k].keys()[y]
        tc[x].append(k)
    for k in d.keys():
        z=max(d[k].values())
        y=d[k].values().index(z)
        x=d[k].keys()[y]
        dc[x].append(k)
#    print 'tens'
#    for v in tc.values():
#        print ' '.join(sorted(v))
#    print 'digits'
#    for v in dc.values():
#        print ' '.join(sorted(v))
    tens[c] = tc.values()
    digits[c] = dc.values()
  for c in ['0','1','2']:
    print c,'tens F-measure:', "%.2f" % fmeasure(truetens,tens[c])
    print c,'tens V-measure:', "%.2f" % vmeasure(truetens,tens[c])
    print c,'tens NVI-measure:', "%.2f" % NVI(truetens,tens[c])
    print c,'digits F-measure:', "%.2f" % fmeasure(truedigits,digits[c])
    print c,'digits V-measure:', "%.2f" % vmeasure(truedigits,digits[c])
    print c,'digits NVI-measure:', "%.2f" % NVI(truedigits,digits[c])
  for c in list(itertools.combinations(['0','1','2'],2)):
    print c[0],c[1],'tens F-measure:', "%.2f" % fmeasure(tens[c[0]],tens[c[1]])
    print c[0],c[1],'tens V-measure:', "%.2f" % vmeasure(tens[c[0]],tens[c[1]])
    print c[0],c[1],'tens NVI-measure:', "%.2f" % NVI(tens[c[0]],tens[c[1]])
    print c[0],c[1],'digits F-measure:',  "%.2f" % fmeasure(digits[c[0]],digits[c[1]])
    print c[0],c[1],'digits V-measure:', "%.2f" % vmeasure(digits[c[0]],digits[c[1]])
    print c[0],c[1],'digits NVI-measure:', "%.2f" % NVI(digits[c[0]],digits[c[1]])
  for c in list(itertools.combinations(['0','1','2'],2)):
    print str("%.2f" % fmeasure(tens[c[0]],tens[c[1]]))+'/'+str("%.2f" % vmeasure(tens[c[0]],tens[c[1]])),
    print '&',
    print str("%.2f" % fmeasure(digits[c[0]],digits[c[1]]))+'/'+str("%.2f" % vmeasure(digits[c[0]],digits[c[1]])),
    print '&',
#    print str("%.2f" % fmeasure(tens[c[0]],tens[c[2]]))+'/'+str("%.2f" % fmeasure(tens[c[0]],tens[c[2]])),
#    print '&',
#    print str("%.2f" % fmeasure(digits[c[0]],digits[c[2]]))+'/'+str("%.2f" % fmeasure(digits[c[0]],digits[c[2]])),
#    print '&',
#    print str("%.2f" % fmeasure(tens[c[1]],tens[c[2]]))+'/'+str("%.2f" % fmeasure(tens[c[1]],tens[c[2]])),
#    print '&',
#    print str("%.2f" % fmeasure(digits[c[1]],digits[c[2]]))+'/'+str("%.2f" % fmeasure(digits[c[1]],digits[c[2]])),
  print '\\\\'
  for c in ['0','1','2']:
    print str("%.2f" % fmeasure(truetens,tens[c[0]]))+'/'+str("%.2f" % vmeasure(truetens,tens[c[0]])),
    print '&',
    print str("%.2f" % fmeasure(truedigits,digits[c[0]]))+'/'+str("%.2f" % vmeasure(truedigits,digits[c[0]])),
    print '&',
#    print str("%.2f" % fmeasure(truetens,tens[c[1]]))+'/'+str("%.2f" % fmeasure(truetens,tens[c[1]])),
#    print '&',
#    print str("%.2f" % fmeasure(truedigits,digits[c[1]]))+'/'+str("%.2f" % fmeasure(truedigits,digits[c[1]])),
#    print '&',
#    print str("%.2f" % fmeasure(truetens,tens[c[2]]))+'/'+str("%.2f" % fmeasure(truetens,tens[c[2]])),
#    print '&',
#    print str("%.2f" % fmeasure(truedigits,digits[c[2]]))+'/'+str("%.2f" % fmeasure(truedigits,digits[c[2]])),
  print '\\\\'

    

def main():
    tabulate(sys.argv[1])


if __name__=='__main__':
    main()

