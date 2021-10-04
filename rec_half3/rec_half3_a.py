import random
import time
DEBUG=True
def generate():
    if DEBUG:
        N=200
        p=[]
        for _ in range(N):
            x,y=[random.randint(0,500) for i in range(2)]
            p.append([x,y])
    else:
        N=int(input())
        p=[list(map(int,input().split())) for i in range(N)]
    return N,p
def dist(x1,y1,x2,y2):
    return ( (x1-x2)**2+(y1-y2)**2 )**0.5
def calc_var(p,c):
    N=len(p)
    ave=0
    for i in range(N):
        idx1,idx2=c[i],c[(i+1)%N]
        x1,y1=p[idx1]
        x2,y2=p[idx2]
        ave+=dist(x1,y1,x2,y2)
    ave/=N
    var=0
    for i in range(N):
        idx1,idx2=c[i],c[(i+1)%N]
        x1,y1=p[idx1]
        x2,y2=p[idx2]
        var+=(ave-dist(x1,y1,x2,y2))**2
    var/=N
    return var
def solve(N,p):
    time0=time.time()
    p_init=[p[i][:] for i in range(N)]
    best_p=[p[i][:]+[i] for i in range(N)]
    best_var=calc_var(p,[i for i in range(N)]) # これを最小化するとよい
    best_ave=0 # 差分を定数で行うのにpreviousが必要
    for i in range(N):
        idx1,idx2=i,(i+1)%N
        x1,y1=p[idx1]
        x2,y2=p[idx2]
        best_ave+=dist(x1,y1,x2,y2)
    best_ave/=N
    while time.time()-time0<1.7:
        idx1=random.randint(1,N-1)
        idx2=random.randint(1,N-1)
        if idx1==idx2:
            continue
        delta=0
        x1,y1,i1=best_p[idx1-1]
        x2,y2,i2=best_p[idx1]
        x3,y3,i3=best_p[(idx1+1)%N]
        x4,y4,i4=best_p[idx2-1]
        x5,y5,i5=best_p[idx2]
        x6,y6,i6=best_p[(idx2+1)%N]
        delta-=(dist(x1,y1,x2,y2)**2+dist(x2,y2,x3,y3)**2)/N
        delta-=(dist(x4,y4,x5,y5)**2+dist(x5,y5,x6,y6)**2)/N
        delta+=best_ave**2
        now_ave=best_ave*N-dist(x1,y1,x2,y2)-dist(x2,y2,x3,y3)-dist(x4,y4,x5,y5)-dist(x5,y5,x6,y6)
        x2,y2,i2,x5,y5,i5=x5,y5,i5,x2,y2,i2
        now_ave+=dist(x1,y1,x2,y2)+dist(x2,y2,x3,y3)+dist(x4,y4,x5,y5)+dist(x5,y5,x6,y6)
        now_ave/=N
        delta+=(dist(x1,y1,x2,y2)**2+dist(x2,y2,x3,y3)**2)/N
        delta+=(dist(x4,y4,x5,y5)**2+dist(x5,y5,x6,y6)**2)/N
        delta-=now_ave**2
        if delta<0:
            best_ave=now_ave
            best_p[idx1],best_p[idx2]=best_p[idx2][:],best_p[idx1][:]
            best_var+=delta
    best_c=[best_p[i][2] for i in range(N)]
    return best_var,best_c
N,p=generate()
best_var,best_c=solve(N,p)
if DEBUG:
    print("best_var:",best_var)
    print("best_sc:",(10**6)/(1+best_var))
else:
    for x in best_c:
        print(x)