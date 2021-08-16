import sys
input=sys.stdin.readline
import random
import time
DEBUG=False
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
    print(ans[:N])