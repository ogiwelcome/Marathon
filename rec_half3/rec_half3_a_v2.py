import random
import time
DEBUG=True
# pre_ansをかなり正確に作る必要がありそう
# 二点間距離の平均を決めて、それになるべく近い点をとっていく貪欲
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
    d=[[0]*N for i in range(N)]
    dd=[[0]*N for i in range(N)]
    for i in range(N):
        x1,y1=p[i]
        for j in range(N):
            x2,y2=p[j]
            dd[i][j]=(x1-x2)**2+(y1-y2)**2
            d[i][j]=dd[i][j]**0.5
    best_ave=0
    max_cnt=0
    for t in range(200,400,5):
        c=0
        for i in range(N):
            for j in range(i):
                if abs(d[i][j]-t)<5:
                    c+=1
        if c>max_cnt:
            max_cnt=c
            best_ave=t
    c=[i for i in range(N)]
    loop=0
    while True:
        loop+=1
        if loop%500==0:
            if time.time()-time0>1.75:
                break
        i=random.randint(0,N-1)
        j=random.randint(0,N-1)
        if i>j:
            i,j=j,i
        d1=d[c[i]][c[i-1]]
        d2=d[c[j]][c[j-1]]
        nd1=d[c[i]][c[j]]
        nd2=d[c[i-1]][c[j-1]]
        if (d1-best_ave)**2+(d2-best_ave)**2>(nd1-best_ave)**2+(nd2-best_ave)**2:
            c=c[:i]+c[i:j][::-1]+c[j:]
    best_c=c[:]
    best_var=calc_var(p,c)
    return best_var,best_c
N,p=generate()
best_var,best_c=solve(N,p)

if DEBUG:
    print("best_var:",best_var)
    print("best_sc:",(10**6)/(1+best_var))
else:
    for x in best_c:
        print(x)