import random
from math import ceil,log
DEBUG=True
def generate():
    if DEBUG:
        N=300
        M=1000
        K=10**8
        A=[random.randint(1,K-1) for i in range(N)]
    else:
        N,M,K=map(int,input().split())
        A=list(map(int,input().split()))
    return N,M,K,A
def calc_score(A,magic_num):
    K=10**8
    s=log(K)*len(A)
    for i in range(len(A)):
        s-=log(A[i]+1)
    sc=ceil(s)
    cnt=0
    for x in A:
        if x!=0:
            cnt+=1
    if cnt<=1:
        sc+=10**8-magic_num
    return sc
def solve(N,M,K,A):
    act=[]
    magic_cnt=0
    for rep in range(M):
        min_v=K
        mp,mq=-1,-1
        for i in range(N):
            for j in range(N):
                v=(A[i]+A[j])%K
                if min_v>v:
                    min_v=v
                    mp=i
                    mq=j
        if mp>=0:
            act.append([mp,mq])
            magic_cnt+=1
            A[mp]=(A[mp]+A[mq])%K
        else:
            break
    if DEBUG:
        print(calc_score(A,magic_cnt))
    else:
        for p,q in act:
            print(p,q)
N,M,K,A=generate()
solve(N,M,K,A)