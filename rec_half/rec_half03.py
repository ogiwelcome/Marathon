import random
from math import ceil,log2
# link:  https://atcoder.jp/contests/rcl-contest-2021/tasks/rcl_contest_2021_a
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
def calc_score_approx(A):
    K=10**8
    s=0
    for a in A:
        s+=min(a+1,K-a)**2
    return s
def calc_minus(A,lim):
    c=0
    for a in A:
        if a>lim:
            c+=1
    return c
def solve(N,M,K,A):
    act=[]
    magic_cnt=0
    lim=K//2
    flg=True
    for rep in range(M):
        minus=calc_minus(A,lim)
        if minus<M-rep-1:
            flg=False
        if flg:
            idx=random.randint(0,N-1)
            mq=-1
            min_v=K
            for i in range(N):
                v=(A[idx]+A[i])%K
                ds=min(v+1,K-v)
                if ds<min_v:
                    min_v=ds
                    mq=i
            if mq>=0:
                act.append([idx,mq])
                A[idx]=(A[idx]+A[mq])%K
                magic_cnt+=1
        else:
            mp=-1
            mq=-1
            min_v=K
            for i in range(N):
                for j in range(i+1):
                    v=(A[i]+A[j])%K
                    if v<min_v:
                        min_v=v
                        mp=i
                        mq=j
            if mp>=0:
                act.append([mp,mq])
                A[mp]=(A[mp]+A[mq])%K
                magic_cnt+=1

    if DEBUG:
        print(calc_score(A,magic_cnt))
    else:
        for p,q in act:
            print(p,q)
N,M,K,A=generate()
solve(N,M,K,A)