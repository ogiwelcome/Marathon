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
# 接続
def merge(st,i,j):
    new_s=[]
    for z in range(len(st)):
        if z!=i and z!=j:
            new_s.append(st[z])
    k=0
    while 0<=k<=min(len(s[i])-1,len(s[j])-1) and st[i][len(s[i])-1-k]==s[j][k]:
        k+=1
    combined=st[i]+st[j][k:]
    new_s.append(combined)
    return new_s
ans=[["."]*N for j in range(N)]

print(len(s))

while True:
    s=erase(s)
    flg=False
    max_idx=[-1,-1]
    max_l=-1
    for k in range(19,-1,-1):
        for i in range(len(s)):
            for j in range(len(s)):
                if i==j:continue
                if len(s[i])>=k and len(s[j])>=k and all(s[i][-z-1]==s[j][z] for z in range(k)):
                    merge_idx=[i,j]
                    flg=True
                    max_l=k
                    break
            if flg:
                break
        if flg:
            break
    if max_l>=5:
        i,j=merge_idx
        s=merge(s,i,j)
    else:
        break

print(len(s))

M=len(s)
s.sort(key=lambda x:len(x),reverse=True)
for ss in s:
    l=len(ss)
    for i in range(N):
        for j in range(N):
            flg=True
            for k in range(l):
                if ans[i][(j+k)%N]!=ss[k] and ans[i][(j+k)%N]!=".":
                    flg=False
            if flg:
                break
        if flg:
            break
    if flg:
        for k in range(l):
            ans[i][(j+k)%N]=ss[k]
max_sc=calc_score(ans)
cnt_loop=0
u=0

print(calc_score(ans))

while time.time()-time0<2.8:
    cnt_loop+=1
    if cnt_loop%2:
        new_ans=[[ans[i][j] for j in range(N)] for i in range(N)]
        x=random.randint(0,N-1)
        y=random.randint(1,N-1)
        new_ans[x]=new_ans[x][y:]+new_ans[x][:y]
        n_sc=calc_score(new_ans)
        if n_sc>max_sc:
            max_sc=n_sc
            ans=[[new_ans[i][j] for j in range(N)] for i in range(N)]
    else:
        new_ans=[[ans[i][j] for j in range(N)] for i in range(N)]
        x=random.randint(0,N-1)
        y=random.randint(0,N-1)
        new_ans[x],new_ans[y]=new_ans[y],new_ans[x]
        n_sc=calc_score(new_ans)
        if n_sc>max_sc:
            max_sc=n_sc
            ans=[[new_ans[i][j] for j in range(N)] for i in range(N)]
#print(cnt_loop)
print(calc_score(ans))

for i in range(N):
    print("".join(ans[i]))