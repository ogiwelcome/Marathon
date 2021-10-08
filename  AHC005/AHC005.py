# 参考実装 https://atcoder.jp/contests/ahc005/submissions/24836272
import random
import heapq
import time
import math
DEBUG=True
def generate():
    if DEBUG:
        N=random.randint(25,35)*2-1
        K=random.randint(2*N,4*N)
        c=[["#"]*N for i in range(N)]
        for rep in range(K):
            d=random.randint(0,1)
            i=random.randint(0,(N-1)//2)*2
            j=random.randint(0,N-1)
            h=random.randint(3,10)
            w=random.randint(5,9)
            for k in range(max(j-h,0),min(j+h,N-1)+1):
                if d==0:
                    c[i][k]=str(w)
                else:
                    c[k][i]=str(w)
        # 最大部分を見つけるパートはDFSorBFSで
        vis=[[0]*N for i in range(N)]
        max_cnt=0
        max_yx=[-1,-1]
        for i in range(N):
            for j in range(N):
                if vis[i][j]:
                    continue
                q=[[i,j]]
                cnt=0
                while q:
                    y,x=q.pop()
                    vis[y][x]=1
                    for ny,nx in [[y-1,x],[y,x-1],[y,x+1],[y+1,x]]:
                        if not (0<=ny<N and 0<=nx<N and vis[ny][nx]==0):
                            continue
                        q.append([ny,nx])
                        vis[ny][nx]=1
                        cnt+=1
                if cnt>max_cnt:
                    max_cnt=cnt
                    max_yx=[i,j]
        # 最大の列挙
        vis=[[0]*N for i in range(N)]
        q=[[max_yx[0],max_yx[1]]]
        while q:
            y,x=q.pop()
            vis[y][x]=1
            for ny,nx in [[y-1,x],[y,x-1],[y,x+1],[y+1,x]]:
                if not (0<=ny<N and 0<=nx<N and vis[ny][nx]==0):
                    continue
                q.append([ny,nx])
        candi=[]
        for i in range(N):
            for j in range(N):
                if vis[i][j]==0:
                    c[i][j]="#"
                else:
                    candi.append([i,j]) # sy,sxの候補
        sy,sx=candi[random.randint(0,len(candi)-1)]
    else:
        N,sy,sx=map(int,input().split())
        c=[list(input()) for i in range(N)]
    return N,sy,sx,c
class Graph:
    def __init__(self,n,directed=False,edges=[]):
        self.n=n
        self.directed=directed
        self.edges=[[] for i in range(self.n)]
        for x,y,cost in edges:
            self.add_edge(x,y,cost)
    def add_edge(self,x,y,cost):
        self.edges[x].append([y,cost])
        if not self.directed:
            self.edges[y].append((x,cost))
    def dijkstra(self,start=None,INF=10**18):
        res=[INF]*self.n
        res[start]=0
        next_set=[(0,start)]
        parent=[-1]*self.n
        parent[start]=-2
        while next_set:
            dist,p=heapq.heappop(next_set)
            if res[p]<dist:
                continue
            for q,cost in self.edges[p]:
                temp_d=dist+cost
                if temp_d<res[q]:
                    res[q]=temp_d
                    heapq.heappush(next_set,(temp_d,q))
                    parent[q]=p
        return res,parent
# Nearest Neighbor 法
def greedy(path,dist):
    size=len(path)
    for i in range(size-1):
        min_len=10000000
        min_pos=0
        for j in range(i+1,size):
            l=dist[path[i]][path[j]]
            if l<min_len:
                min_len=l
                min_pos=j
        path[i+1],path[min_pos]=path[min_pos],path[i+1]
    return path
# 2-opt 法
def opt_2(path,dist):
    total=0
    size=len(path)
    while True:
        cnt=0
        for i in range(size-2):
            i1=i+1
            for j in range(i+2,size):
                j1=(j+1)%size
                if i!=0 or j1!=0:
                    d1=dist[path[i]][path[i1]]
                    d2=dist[path[j]][path[j1]]
                    d3=dist[path[i]][path[j]]
                    d4=dist[path[i1]][path[j1]]
                    if d1+d2>d3+d4:
                        new_path=path[i1:j+1]
                        path[i1:j+1]=new_path[::-1]
                        cnt+=1
        total+=cnt
        if cnt==0:
            break
    return path,total
##############################
time0=time.time()
N,sy,sx,c=generate()
grid=[]
for i in range(N):
    for j in range(N):
        if c[i][j]=="#":
            grid.append(-1)
        else:
            grid.append(int(c[i][j]))
# 交差点の場所を列挙
rep=[[sy*N+sx]]
for i in range(N):
    tmp=[]
    for j in range(N):
        if grid[i*N+j]==-1:
            if tmp and j>=2 and grid[i*N+j-2]!=-1:
                # 3#4みたいな形になってる
                rep.append(tmp)
            tmp=[]
        elif (i<=N-2 and grid[(i+1)*N+j]!=-1) or (i>=1 and grid[(i-1)*N+j]!=-1):
            # 上下で繋がってる
            tmp.append(i*N+j)
    if tmp and grid[i*N+N-2]!=-1:
        rep.append(tmp)
for j in range(N):
    tmp=[]
    for i in range(N):
        if grid[i*N+j]==-1:
            if tmp and i>=2 and grid[(i-2)*N+j]!=-1:
                # 3#4みたいな形になってる(縦)
                rep.append(tmp)
            tmp=[]
        elif (j<=N-2 and grid[i*N+j+1]!=-1) or (j>=1 and grid[i*N+j-1]!=-1):
            # 左右で繋がってる
            tmp.append(i*N+j)
    if tmp and grid[(N-2)*N+j]!=-1:
        rep.append(tmp)

G=Graph(N*N,directed=True)
for i in range(N):
    for j in range(N):
        p=i*N+j
        if grid[p]==-1:
            continue
        for ny,nx in [[i-1,j],[i+1,j],[i,j-1],[i,j+1]]:
            if not (0<=ny<N and 0<=nx<N and grid[ny*N+nx]!=-1):
                continue
            q=ny*N+nx
            G.add_edge(p,q,grid[q])
dist=[[] for i in range(N*N)]
parent=[[] for i in range(N*N)]
for i in range(N):
    for j in range(N):
        p=i*N+j
        if grid[p]==-1:
            continue
        dist[p],parent[p]=G.dijkstra(start=p)
def score(path):
    res=0
    for p in path:
        res+=grid[p]
    return res

INF=10**18
dir={(1,0):"D",(0,1):"R",(-1,0):"U",(0,-1):"L"}
S=10**18
P0=[0]*len(rep)
S0=10**18
ans=[]
while time.time()-time0<2.8:
    decode=[] # ?
    code={} # ?
    P=P0[:]
    i0=random.randint(0,len(rep)-1)
    for i,r in enumerate(rep):
        if i==i0:
            P[i]+=1
            P[i]%=len(rep[i])
        decode.append(r[P[i]])
        code[P[i]]=len(code)
    if P==P0:
        continue
    L=len(decode)
    dist_tab=[[INF]*L for i in range(L)]
    for i in range(L):
        if grid[decode[i]]==-1:
            continue
        for j in range(L):
            dist_tab[i][j]=dist[decode[i]][decode[j]]
    path=list(range(L))
    path=greedy(path,dist_tab)
    path,cnt=opt_2(path,dist_tab)

    path.append(0)
    path2=[]
    res=[]
    for i in range(L):
        start,p0=decode[path[i]],decode[path[i+1]]
        route=[]
        tmp=[]
        while p0!=start:
            p=parent[start][p0]
            #print(p0,p)
            y0,x0=p0//N,p0%N
            y,x=p//N,p%N
            dy,dx=y0-y,x0-x
            route.append(dir[(dy,dx)])
            tmp.append(p)
            p0=p
        route.reverse()
        res.extend(route)
        tmp.reverse()
        path2.extend(tmp)
    now_s=score(path2)
    if S>=now_s:
        prob=1
    else:
        prob=math.exp( (S-now_s)*2.8/((time.time()-time0)*5) )
    if random.random()<=prob:
        P0=P
        S=now_s
    if now_s<S0:
        ans=res
        S0=now_s
print("".join(ans))