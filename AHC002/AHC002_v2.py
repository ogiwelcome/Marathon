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
def nxt_tile(y,x):
    arr=[]
    if x>0:
        arr.append([y,x-1])
    if x<N-1:
        arr.append([y,x+1])
    if y>0:
        arr.append([y-1,x])
    if y<N-1:
        arr.append([y+1,x])
    #arr.sort(key=lambda x:min(x[0],N-1-x[0],x[1],N-1-x[1])) 
    random.shuffle(arr)# とりあえずここで乱択
    return arr
def dir(p1,p2):
    y1,x1=p1
    y2,x2=p2
    if y1==y2 and x1==x2-1:
        return "R"
    if y1==y2 and x1==x2+1:
        return "L"
    if y1==y2-1 and x1==x2:
        return "D"
    if y1==y2+1 and x1==x2:
        return "U"
dy=[1,0,-1,0]
dx=[0,1,0,-1]
ans_path=""
max_sc=0
def dfs(y,x,path,vis,sc):
    global ans_path,max_sc
    if time.time()-time0>1.8:
        return
    vis.add(t[y][x])
    update=False
    for py,px in nxt_tile(y,x):
        if t[py][px] in vis:
            continue
        update=True
        now_sc=sc+p[py][px]
        now_path=path+dir([y,x],[py,px])
        dfs(py,px,now_path,vis,now_sc)
    if not update:
        if sc>max_sc:
            max_sc=sc
            ans_path=path
dfs(sy,sx,"",set(),p[sy][sx])
print(ans_path)