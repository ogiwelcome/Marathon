# とりあえず写経してみて空気をつかむ
import random
import sys
input=sys.stdin.readline
import math
import time
time_lim=2.8
start_temp=50
end_temp=10
DEBUG=True
if DEBUG:
    N=30
    b1=random.randint(10,19)
    b2=random.randint(20,29)
    b3=random.randint(30,39)
    B=[b1,b2,b3]
    L=[[random.randint(1,9) for j in range(N)] for i in range(N)]
    R=[[random.randint(1,9) for j in range(N)] for i in range(N)]
    for i in range(N):
        for j in range(N):
            if L[i][j]>R[i][j]:
                L[i][j],R[i][j]=R[i][j],L[i][j]
else:
    N,b1,b2,b3=map(int,input().split())
    B=[b1,b2,b3]
    L=[list(map(int,input().split())) for i in range(N)]
    R=[list(map(int,input().split())) for i in range(N)]
start_time=time.time()
end_time=start_time+time_lim
candi=[]
for i in range(N):
    for j in range(N):
        if L[i][j]!=R[i][j]:
            candi.append((i,j))
def now_temp(now_time):
    return start_temp+(end_temp-start_temp)*(now_time-start_time)/time_lim
def prob(new_ans,pre_ans,temp):
    return math.exp((new_ans-pre_ans)/temp)
def make_F_rand():
    a=[[0]*N for i in range(N)]
    for i in range(N):
        for j in range(N):
            a[i][j]=random.randint(L[i][j],R[i][j])
    s0=[[0]*(N+1) for i in range(N)]
    s1=[[0]*(N+1) for i in range(N)]
    for i in range(N):
        for j in range(N):
            s0[i][j+1]=s0[i][j]+a[i][j]
            s1[i][j+1]=s1[i][j]+a[j][i]
    return a,s0,s1
def calc_pt(s0,s1):
    p0=[0]*N
    p1=[0]*N
    for r in range(N):
        for i in range(N+1):
            for j in range(i+2,N+1):
                v0=s0[r][j]-s0[r][i]
                v1=s1[r][j]-s1[r][i]
                if v0 in B:
                    p0[r]+=v0
                if v1 in B:
                    p1[r]+=v1
    return p0,p1
def change_test_and_calc(i,j,x,pre_ans):
    ai=[a[i][r] for r in range(N)]
    aj=[a[r][j] for r in range(N)]
    ai[j]=x
    aj[i]=x
    si=[0]
    sj=[0]
    for k in range(N):
        si.append(si[-1]+ai[k])
        sj.append(sj[-1]+aj[k])
    pi=0
    pj=0
    for p in range(N+1):
        for q in range(p+2,N+1):
            vi=si[q]-si[p]
            vj=sj[q]-sj[p]
            if vi in B:
                pi+=vi
            if vj in B:
                pj+=vj
    new_ans=pre_ans-p0[i]-p1[j]+pi+pj
    change_prob=prob(new_ans,pre_ans,now_temp(time.time()))
    u=random.random()
    if u<change_prob:
        a[i][j]=x
        p0[i]=pi
        p1[j]=pj
        s0[i]=si[:]
        s1[j]=sj[:]
        pre_ans=new_ans
    return pre_ans
a,s0,s1=make_F_rand()
p0,p1=calc_pt(s0,s1)
pre_ans=sum(p0)+sum(p1)
while time.time()<end_time:
    k=random.randint(0,len(candi)-1)
    i,j=candi[k]
    x=random.randint(L[i][j],R[i][j])
    pre_ans=change_test_and_calc(i,j,x,pre_ans)
for i in range(N):
    print(*a[i])