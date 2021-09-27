import sys
input=sys.stdin.readline
import random
import time
DEBUG=True
def generate():
    if DEBUG:
        arr=[]
        N=20
        for i in range(N):
            for j in range(N):
                arr.append([i,j])
        random.shuffle(arr)
        p=[arr[i][:] for i in range(100)]
    else:
        N=20
        p=[list(map(int,input().split())) for i in range(100)]
    return N,p

def calc_score(path,p):
    nx,ny=0,0
    idx=0
    for dd in path:
        if dd=="R":
            ny+=1
        elif dd=="L":
            ny-=1
        elif dd=="U":
            nx-=1
        elif dd=="D":
            nx+=1
        if dd=="I" and idx<len(p) and p[idx][0]==nx and p[idx][1]==ny:
            idx+=1
    if idx<100:
        return 0
    else:
        return 4000-len(path)
def solve(N,P):
    ans=[]
    p=[[0,0]]+P
    lp=len(p)
    for i in range(lp-1):
        px,py=p[i]
        nx,ny=p[i+1]
        dx=nx-px
        dy=ny-py
        if dy>0:
            for j in range(dy):
                ans.append("R")
        else:
            for j in range(abs(dy)):
                ans.append("L")
        if dx>0:
            for j in range(dx):
                ans.append("D")
        else:
            for j in range(abs(dx)):
                ans.append("U")
        ans.append("I")
    return "".join(ans)
N,P=generate()
ans=solve(N,P)
if DEBUG:
    print(calc_score(ans,P))
else:
    print(ans)