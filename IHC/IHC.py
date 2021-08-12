import sys
input=sys.stdin.readline
import random
import time
from heapq import heappop,heappush
time0=time.time()
DEBUG=True
if DEBUG:
    D=365
    c=[random.randint(0,100) for i in range(26)]
    s=[[random.randint(0,20000) for j in range(26)] for i in range(D)]
else:
    D=int(input())
    c=list(map(int,input().split()))
    s=[list(map(int,input().split())) for i in range(D)]
# score関数は改良できる->scoreをそれぞれのtypeで分けておくことで
# swap操作前後で定数で遷移できる
def calc_score(arr):
    last=[0]*26
    sc=0
    for d in range(D):
        last[arr[d]-1]=d+1
        sc+=s[d][arr[d]-1]
        for i in range(26):
            sc-=c[i]*(d+1-last[i])
    return sc
def estimate(arr,delay): # 1-indexed
    last=[0]*26
    sc=0
    for d in range(len(arr)):
        last[arr[d]-1]=d+1
        for i in range(26):
            sc-=(d+1-last[i])*c[i]
        sc+=s[d][arr[d]-1]
    for d in range(len(arr),min(len(arr)+delay,D)):
        for i in range(26):
            sc-=(d+1-last[i])*c[i]
    return sc
out=[]
last=[0]*26
now_sc=0
delay=10
for i in range(D):
    best_idx=0
    max_sc=-10**9
    for j in range(26):
        out.append(j+1)
        sc=estimate(out,delay)
        if max_sc<sc:
            max_sc=sc
            best_idx=j
        out.pop()
    out.append(best_idx+1)
print(*out,sep="\n")