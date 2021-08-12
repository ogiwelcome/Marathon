import sys
import random
import time
import heapq as hq
input=sys.stdin.readline
time0=time.time()
DEBUG=True
if DEBUG:
    N=50
    sy,sx=[random.randint(0,N-1) for i in range(2)]
    t=[[i*N+j for j in range(N)] for i in range(N)]
    flag=[[0]*N for i in range(N)]
    arr=[(1,0),(0,1),(-1,0),(0,-1)]
    for i in range(N):
        for j in range(N):
            if flag[i][j]:
                continue
            u=random.randint(0,3)
            for l in range(4):
                dy,dx=arr[(u+l)%4]
                ny,nx=i+dy,j+dx
                if not (0<=ny<N and 0<=nx<N):
                    continue
                if flag[ny][nx]==0:
                    flag[ny][nx]=flag[i][j]=1
                    t[i][j]=t[ny][nx]
                    break
    s=set()
    for i in range(N):
        for j in range(N):
            s.add(t[i][j])
    s=sorted(list(s))
    relation={}
    cnt=0
    for x in s:
        relation[x]=cnt
        cnt+=1
    for i in range(N):
        for j in range(N):
            t[i][j]=relation[t[i][j]]
    p=[[random.randint(0,99) for j in range(N)] for i in range(N)]
else:
    sy,sx=map(int,input().split())
    N=50
    t=[list(map(int,input().split())) for i in range(N)]
    p=[list(map(int,input().split())) for i in range(N)]

modify=200 # 補正値
best_sc=[[-1]*N for i in range(N)]
max_sc=0
ans=""
q=[(sy,sx,0,"",set([t[sy][sx]]))]
while q:
    if time.time()-time0>1.8:break
    y,x,pre_sc,path,vis=hq.heappop(q)
    if -pre_sc>max_sc:
        max_sc=-pre_sc
        ans=path
    for ny,nx,nxt_dir in ( (y-1,x,"U"),(y+1,x,"D"),(y,x-1,"L"),(y,x+1,"R") ):
        if not (0<=ny<N and 0<=nx<N):continue
        if t[ny][nx] in vis:continue
        now_sc=pre_sc-p[ny][nx]
        tmp_best=best_sc[ny][nx]
        if -pre_sc<tmp_best-modify:
            continue
        best_sc[ny][nx]=max(tmp_best,-now_sc)
        now_path=path+nxt_dir
        now_vis=vis|set([t[ny][nx]])
        hq.heappush(q,(ny,nx,now_sc,now_path,now_vis))
print("".join(ans))