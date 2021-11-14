import random
import time
DEBUG=True
def dist(sy,sx,ty,tx):
    return abs(sy-ty)+abs(sx-tx)
def generate():
    if DEBUG:
        tasks=[]
        N=1000
        while len(tasks)<N:
            a,b,c,d=[random.randint(0,800) for i in range(4)]
            if dist(a,b,c,d)>=100:
                tasks.append([a,b,c,d])
    else:
        N=1000
        tasks=[list(map(int,input().split())) for i in range(N)]
    return N,tasks
def solve(N,tasks):
    time0=time.time()
    # 初期解生成
    # とりあえず始点まわり
    tasks=[tasks[i]+[i] for i in range(N)]
    tasks.sort(key=lambda x:abs(400-x[0])+abs(400-x[1])+abs(400-x[2])+abs(400-x[3]))
    route=tasks[:50]
    route1=[[route[i][0],route[i][1],route[i][4]] for i in range(50)]
    route2=[[route[i][2],route[i][3],route[i][4]] for i in range(50)]
    min_dist=0
    # 最初と最後はめんどいから放置
    a0,b0,idx0=route1[0]
    c1,d1,idx1=route2[-1]
    min_dist+=dist(400,400,a0,b0)+dist(c1,d1,400,400)
    #
    for i in range(len(route1)-1):
        a1,b1,_=route1[i]
        a2,b2,_=route1[i+1]
        min_dist+=dist(a1,b1,a2,b2)
        c1,d1,_=route2[i]
        c2,d2,_=route2[i+1]
        min_dist+=dist(c1,d1,c2,d2)
    loop=0
    while True:
        loop+=1
        if loop%100==0 and time.time()-time0>0.7:
            break
        # まず隣接swap
        idx=random.randint(1,47)
        a0,b0,idx0=route1[idx-1]
        a1,b1,idx1=route1[idx] # この二つ
        a2,b2,idx2=route1[idx+1] #
        a3,b3,idx3=route1[idx+2]
        # 差分
        delta=0
        delta-=dist(a0,b0,a1,b1)+dist(a2,b2,a3,b3)
        a1,b1,a2,b2=a2,b2,a1,b1
        delta+=dist(a0,b0,a1,b1)+dist(a2,b2,a3,b3)
        if delta<0:
            route1[idx],route1[idx+1]=route1[idx+1],route1[idx]
            min_dist+=delta
    loop=0
    while True:
        loop+=1
        if loop%100==0 and time.time()-time0>1.4:
            break
        # まず隣接swap
        idx=random.randint(1,47)
        c0,d0,idx0=route2[idx-1]
        c1,d1,idx1=route2[idx] # この二つ
        c2,d2,idx2=route2[idx+1] #
        c3,d3,idx3=route2[idx+2]
        # 差分
        delta=0
        delta-=dist(c0,d0,c1,d1)+dist(c2,d2,c3,d3)
        c1,d1,c2,d2=c2,d2,c1,d1
        delta+=dist(c0,d0,c1,d1)+dist(c2,d2,c3,d3)
        if delta<0:
            route2[idx],route2[idx+1]=route2[idx+1],route2[idx]
            min_dist+=delta
    route_idx=[route[i][4]+1 for i in range(len(route))]
    if DEBUG:
        score=int((10**8)/(1000+min_dist))
        print("score:",score)
    else:
        print(len(route_idx),*route_idx)
        arr=[]
        arr+=[400,400]
        for a,b,_ in route1:
          arr+=[a,b]
        for c,d,_ in route2:
          arr+=[c,d]
        arr+=[400,400]
        cnt=len(arr)//2
        print(cnt,*arr)
N,tasks=generate()
solve(N,tasks)