import random
from math import ceil,log2
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
    s=log2(K)*len(A)
    for i in range(len(A)):
        s-=log2(A[i]+1)
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
    for i in range(N):
        B=A[:]
        min_v=K
        mq=-1
        mq1=-1
        mq2=-1
        for j in range(N):
            v=(A[i]+A[j])%K
            if v<min_v:
                min_v=v
                mq=j
        for j in range(N):
            for k in range(j+1):
                v=(A[i]+A[j]+A[k])%K
                if v<min_v:
                    mq1=j
                    mq2=k
                    min_v=v
                    mq=-1
        if mq>=0:
            magic_cnt+=1
            act.append([i,mq])
            A[i]=(A[i]+A[mq])%M
        elif mq1>=0:
            magic_cnt+=2
            act.append([i,mq1])
            act.append([i,mq2])
            A[i]=(A[i]+A[mq1]+A[mq2])%M
    if DEBUG:
        print(calc_score(A,magic_cnt))
    else:
        for p,q in act:
            print(p,q)
N,M,K,A=generate()
solve(N,M,K,A)