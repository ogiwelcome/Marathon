import random
DEBUG=True
def generate():
    if DEBUG:
        N,K=100,9
        s=[[random.randint(1,K) for i in range(N)] for j in range(N)]
    else:
        _,N,K=map(int,input().split())
        s=[list(map(int,input())) for i in range(N)]
    return N,K,s
def dfs_cnt(sy,sx,grid):
    # (y,x)からカウントして同色である部分を調べたのち、それに隣接する色をカウント
    N,K=100,9
    cnt=[0]*(K+1)
    q=[[sy,sx]]
    vis=[[0]*N for i in range(N)]
    target=grid[sy][sx]
    vis[sy][sx]=1
    while q:
        y,x=q.pop()
        for ny,nx in [[y-1,x],[y+1,x],[y,x-1],[y,x+1]]:
            if not (0<=ny<N and 0<=nx<N and vis[ny][nx]==0):
                continue
            if grid[ny][nx]==target:
                q.append([ny,nx])
                vis[ny][nx]=1
            else:
                cnt[grid[ny][nx]]+=1
                vis[ny][nx]=1
    return cnt
def dfs_coloring(sy,sx,grid,col):
    N,K=100,9
    q=[[sy,sx]]
    vis=[[0]*N for i in range(N)]
    before=grid[sy][sx]
    while q:
        y,x=q.pop()
        if grid[y][x]==before:
            grid[y][x]=col
            for ny,nx in [[y-1,x],[y+1,x],[y,x-1],[y,x+1]]:
                if not (0<=ny<N and 0<=nx<N and vis[ny][nx]==0):
                    continue
                q.append([ny,nx])
                vis[ny][nx]=1
    return grid
def solve(N,K,s):
    actions=[]
    lim=10000
    ty,tx=49,49
    for rep in range(500):
        cnt=dfs_cnt(ty,tx,s)
        if max(cnt)==0:
            break
        col=cnt.index(max(cnt))
        actions.append([ty+1,tx+1,col])
        s=dfs_coloring(ty,tx,s,col)
        #print(rep,max(cnt))
    return actions
N,K,s=generate()
actions=solve(N,K,s)
if DEBUG:
    print("predicted score:",( 100*(N*N)-len(actions) )*50)
    print(len(actions))
    for x in actions:
        print(*x)
else:
    print(len(actions))
    for x in actions:
        print(*x)