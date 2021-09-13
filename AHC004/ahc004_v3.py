# TODO: 
# mergeした回数順で置いていく
# 先にloopを作っておいて埋めておく
import sys
input=sys.stdin.readline
import random
import time
DEBUG=True
al=list("ABCDEFGH")
time0=time.time()
if DEBUG:
    N=20
    a=[[al[random.randint(0,len(al)-1)] for i in range(N)] for j in range(N)]
    L=random.randint(4,10)
    M=random.randint(400,800)
    s=[]
    for _ in range(M):
        y=random.randint(0,N-1)
        x=random.randint(0,N-1)
        d=random.randint(0,1)
        k=random.randint(L-2,L+2)
        if d==0:
            ss=[]
            for j in range(k):
                ss.append(a[y][(x+j)%N])
            s.append("".join(ss))
        else:
            ss=[]
            for i in range(k):
                ss.append(a[(y+i)%N][x])
            s.append("".join(ss))
else:
    N,M=map(int,input().split())
    s=[input().rstrip() for i in range(M)]
s_init=s[:] # scoring用
def erase(st):
    skip=[0]*len(s)
    for i in range(len(s)):
        for j in range(len(s)):
            if i!=j and s[i] in s[j]:
                skip[i]=1
                break
            elif i!=j and len(s[j])==20 and s[i] in s[j]*2:
                skip[i]=1
                break
    new_s=[]
    for i in range(len(s)):
        if not skip[i]:
            new_s.append(s[i])
    return new_s
s=erase(s)
M=len(s)
candi=[]
b=[[0]*M for i in range(M)]
for i in range(M):
    si=s[i]
    for j in range(M):
        if i==j:
            b[i][j]=-1
            continue
        sj=s[j]
        for k in range(len(sj),0,-1):
            if len(si)>=k and si[-k:]==sj[:k]:
                candi.append([k,i,j])
                b[i][j]=k
                break
        else:
            b[i][j]=-1
candi.sort(reverse=True)
flg=[0]*M # used or not
idx=0
res=[]
for _ in range(N):
    while True:
        l,i,j=candi[idx]
        if flg[i]==flg[j]==0:
            ans=s[i]+s[j][l:]
            idx+=1
            flg[j]=1
            flg[i]=1
            break
        else:
            idx+=1
    # j->lastで使ったやつに何つけるか
    while True:
        z=[[b[j][k],k] for k in range(M)]
        z.sort(reverse=True)
        for bb,k in z:
            if flg[k] or bb==-1:continue
            ans+=s[k][bb:]
            j=k
            flg[k]=1
            break
        if len(ans)>N:break
    res.append(ans[:N])
# 局所探索+scoring
def calc_score(arr):
    candi=[]
    for i in range(N):
        candi.append("".join(arr[i])*2)
    for i in range(N):
        tmp=[arr[j][i] for j in range(N)]
        candi.append("".join(tmp)*2)
    c=0
    for ss in s_init:
        for xx in candi:
            if ss in xx:
                c+=1
                break
    return round(c*10**8/M)
max_sc=calc_score(res)
cnt_loop=0
print(max_sc)
while time.time()-time0<2.75:
    cnt_loop+=1
    if cnt_loop%2:
        new_res=[[res[i][j] for j in range(N)] for i in range(N)]
        x=random.randint(0,N-1)
        y=random.randint(1,N-1)
        new_res[x]=new_res[x][y:]+new_res[x][:y]
        n_sc=calc_score(new_res)
        if n_sc>max_sc:
            max_sc=n_sc
            res=[[new_res[i][j] for j in range(N)] for i in range(N)]
    else:
        new_res=[[res[i][j] for j in range(N)] for i in range(N)]
        x=random.randint(0,N-1)
        y=random.randint(0,N-1)
        new_res[x],new_res[y]=new_res[y],new_res[x]
        n_sc=calc_score(new_res)
        if n_sc>max_sc:
            max_sc=n_sc
            res=[[new_res[i][j] for j in range(N)] for i in range(N)]
print(cnt_loop)
print(calc_score(res))
for i in range(N):
    print("".join(res[i]))