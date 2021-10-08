# 二次元gridにおけるTSP(巡回セールスマン問題)について考察する
# とりあえずgeneratorは(y,x)形式でN Nodeを指定
# 最短経路は直線でOK(平行移動にはしない)
import random
def generate():
    N=50
    p=set()
    for _ in range(N):
        y,x=[random.randint(0,N-1) for i in range(2)]
        while (y,x) in p:
            y,x=[random.randint(0,N-1) for i in range(2)]
        p.add((y,x))
    p=list(p)
    return N,p
# N -> サイズ
# path -> i番目のidx
# dist -> 二次元配列
def or_opt(N,path,dist):
    tot=0
    while True:
        cnt=0
        for i in range(N):
            i0=(i-1)%N
            i1=(i+1)%N
            for j in range(N):
                j1=(j+1)%N
                if j!=i and j1!=i:
                    # i0 - i - i1 
                    # j - j1
                    d1=dist[path[i0]][path[i]]
                    d2=dist[path[i]][path[i1]]
                    d3=dist[path[j]][path[j1]]
                    d4=dist[path[i0]][path[i1]]
                    d5=dist[path[j]][path[i]]
                    d6=dist[path[i]][path[j1]]
                    # i0 - i1
                    # j - i - j1
                    if d1+d2+d3>d4+d5+d6:
                        idx=path[i]
                        path[i:i+1]=[]
                        if i<j:
                            path[j:j]=[idx]
                        else:
                            path[j1:j1]=[idx]
                        cnt+=1
        tot+=cnt
        if cnt==0:
            break
    return path,tot
def solve(N,p):
    d=[[0]*N for i in range(N)]
    for i in range(N):
        for j in range(N):
            y1,x1=p[i]
            y2,x2=p[j]
            d[i][j]=((x1-x2)**2+(y1-y2)**2)**0.5
    path,tot=or_opt(N,[i for i in range(N)],d)
    ans_d=0
    for i in range(N-1):
        ans_d+=d[path[i]][path[i+1]]
    return path,tot,ans_d
ave=0
for rep in range(10):
    N,p=generate()
    path,tot,ans_d=solve(N,p)
    ave+=ans_d
ave/=10
print("average_calc_distance",ave)