import sys
import random
import time
input=sys.stdin.readline
DEBUG=True
time0=time.time()
if DEBUG:
    N=30
    b1=random.randint(10,19)
    b2=random.randint(20,29)
    b3=random.randint(30,39)
    b=[b1,b2,b3]
    l=[[random.randint(1,9) for j in range(N)] for i in range(N)]
    r=[[random.randint(1,9) for j in range(N)] for i in range(N)]
    for i in range(N):
        for j in range(N):
            if l[i][j]>r[i][j]:
                l[i][j],r[i][j]=r[i][j],l[i][j]
else:
    N,b1,b2,b3=map(int,input().split())
    b=[b1,b2,b3]
    l=[list(map(int,input().split())) for i in range(N)]
    r=[list(map(int,input().split())) for i in range(N)]
def calc_score_changed(a,y,x,v):
    e=[[a[i][j] for j in range(N)] for i in range(N)]
    e[y][x]=v
    cnt=[0]*3
    cum_a_yoko=[0]+[a[y][j] for j in range(N)]
    cum_e_yoko=[0]+[e[y][j] for j in range(N)]
    cum_a_tate=[0]+[a[j][x] for j in range(N)]
    cum_e_tate=[0]+[e[j][x] for j in range(N)]
    for i in range(N):
        cum_a_yoko[i+1]+=cum_a_yoko[i]
        cum_a_tate[i+1]+=cum_a_tate[i]
        cum_e_yoko[i+1]+=cum_e_yoko[i]
        cum_e_tate[i+1]+=cum_e_tate[i]
    for l in range(N):
        for r in range(l,N):
            for k in range(3):
                if not l<=x<=r:
                    continue
                if cum_a_yoko[r+1]-cum_a_yoko[l]==b[k]:
                    cnt[k]-=1
                if cum_e_yoko[r+1]-cum_e_yoko[l]==b[k]:
                    cnt[k]+=1
    for l in range(N):
        for r in range(l,N):
            for k in range(3):
                if not l<=y<=r:
                    continue
                if cum_a_tate[r+1]-cum_a_tate[l]==b[k]:
                    cnt[k]-=1
                if cum_e_tate[r+1]-cum_e_tate[l]==b[k]:
                    cnt[k]+=1
    d_sc=b[0]*cnt[0]+b[1]*cnt[1]+b[2]*cnt[2]
    if d_sc>0:
        return e
    else:
        return a
def calc_score_init(a):
    cnt=[0]*3
    for i in range(N):
        for l in range(1,N):
            for r in range(l,N):
                for k in range(3):
                    if sum(a[i][:r+1])-sum(a[i][:l])==b[k]:
                        cnt[k]+=1
        for r in range(N):
            for k in range(3):
                if sum(a[i][:r+1])==b[k]:
                    cnt[k]+=1
    a=[[a[i][j] for i in range(N)] for j in range(N)]
    for i in range(N):
        for l in range(1,N):
            for r in range(l,N):
                for k in range(3):
                    if sum(a[i][:r+1])-sum(a[i][:l])==b[k]:
                        cnt[k]+=1
        for r in range(N):
            for k in range(3):
                if sum(a[i][:r+1])==b[k]:
                    cnt[k]+=1
    res=cnt[0]*b[0]+cnt[1]*b[1]+cnt[2]*b[2]
    return res
# 初期解生成
c=[[l[i][j] for j in range(N)] for i in range(N)]
for i in range(N):
    for j in range(N):
        for bi in b[::-1]:
            for k in range(1,j):
                tmp1=bi-sum(c[i][j-k:j])
                if l[i][j]<=tmp1<=r[i][j]:
                    c[i][j]=tmp1
            for k in range(1,i):
                tmp2=bi
                for m in range(i-k,i):
                    tmp2-=c[m][j]
                if l[i][j]<=tmp2<=r[i][j]:
                    c[i][j]=tmp2
print(calc_score_init(c))
cnt_loop=0
while True:
    cnt_loop+=1
    if cnt_loop%100==0:
        if time.time()-time0>2.75:
            break
    y=random.randint(0,N-1)
    x=random.randint(0,N-1)
    v=random.randint(l[y][x],r[y][x])
    c=calc_score_changed(c,y,x,v)
#print(cnt_loop)
print(calc_score_init(c))
for i in range(N):
    print(*c[i])