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
def solve(N,M,K,A):
    INF=10**18
    act=[]
    magic_cnt=0
    over_half=0
    for a in A:
        if a>K//2:
            over_half+=1
    for rep in range(M):
        if M-over_half-2<=rep:
            break
        min_sc=INF
        idx=(-1,-1)
        for i in range(N):
            for j in range(N):
                ai=A[i]
                aj=A[j]
                aij=(ai+aj)%K
                sc=min(aij+1,K-aij)-min(ai+1,K-ai)
                if sc<min_sc:
                    min_sc=sc
                    idx=(i,j)
        p,q=idx
        if A[p]>K//2 and (A[p]+A[q])%K<=K//2:
            over_half-=1
        if A[p]<=K//2 and (A[p]+A[q])%K>K//2:
            over_half+=1
        A[p]=(A[p]+A[q])%K
        act.append([p,q])
        magic_cnt+=1
    for i in range(N):
        if A[i]<=K//2:continue
        now=10**18
        idx=-1
        for j in range(N):
            if (A[i]+A[j])%K<now:
                now=(A[i]+A[j])%K
                idx=j
        if idx>=0:
            A[i]=(A[i]+A[idx])%K
            act.append([i,idx])
            magic_cnt+=1
    if DEBUG:
        print(calc_score(A,magic_cnt))
    else:
        for p,q in act:
            print(p,q)
N,M,K,A=generate()
solve(N,M,K,A)