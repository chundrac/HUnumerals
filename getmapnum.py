#!usr/bin/env python

import sys
from collections import defaultdict

IPA = {'A':'{\\textscripta}',
'An':'\\~{\\textscripta}',
'E':'e',
'I':'i',
'i':'I',
'R':'\\:r',
'T':'\\:t',
'Th':'\\:t\\textsuperscript{h}',
'a':'@',
'ain':'\\~{\\ae}',
'au':'O',
'aun':'\\~O',
'ch':'c\\textsuperscript{h}',
'e':'E',
'y':'j'}

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
formdict = {}
numdict = {}
for l in text:
    w = l[1]
    IPAw = []
    for s in w:
        if s in IPA.keys():
            IPAw.append(IPA[s])
        else:
            IPAw.append(s)
    forms.append(tuple(IPAw))
    formdict[''.join(w)] = tuple(IPAw)
    numdict[''.join(w)] = text.index(l)+10
#    numdict[''.join(w)] = tuple([int(l[0].split()[0]),int(l[0].split()[1])])


def tabulate(fn,c):
    m = []
    for l in open(fn,'r'):
        m.append(l.split())
    t = defaultdict()
    d = defaultdict()
    mu = defaultdict()
    for l in m:
        t[l[1]] = defaultdict(int)
        d[l[1]] = defaultdict(int)
        mu[l[1]] = defaultdict(int)
    for l in m:
        if l[0]==c:
            t[l[1]][l[3]] = int(l[-1])
            d[l[1]][l[4]] = int(l[-1])
            mu[l[1]][l[2]] = int(l[-1])
    for k in mu.keys():
        mu[k]=int(sorted(mu[k].keys(),key=lambda(x):mu[k][x])[-1])
#    print mu
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
    tv = {}
    dv = {}
    for k in tc.keys():
        for w in tc[k]:
            tv[w]=k
    for k in dc.keys():
        for w in dc[k]:
            dv[w]=k
    ind = defaultdict(list)
    for k in tv.keys():
#        print k
#        print ''.join(list(formdict[k][:mu[k]])+['|']+list(formdict[k][mu[k]:]))
        ind[(int(tv[k])-1,int(dv[k])-1)].append('$'+str(numdict[k])+'$')
#    print len(tc.keys())
    c = []
    for i in range(9):
        l = []
        for j in range(len(dc.keys())):
            l.append('')
        c.append(l)
#    print c
#    print ind
    for k in ind.keys():
#        print k,[k[0]],[k[1]],ind[k]
        c[k[0]][k[1]] = ', '.join(ind[k])
    print '\\hline'
    for l in c:
        print ' & '.join(l)+'\\\\'
        print '\\hline'


def main():
    tabulate(sys.argv[1],sys.argv[2])


if __name__=='__main__':
    main()

