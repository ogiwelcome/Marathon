import random
import time
DEBUG=False
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
    # どこを中心に動くか決める
    best_y=-1
    best_x=-1
    min_sc=10**9
    for i in range(0,801,40):
        for j in range(0,801,40):
            cnt=0
            tasks.sort(key=lambda x:abs(i-x[0])**2+abs(j-x[1])**2+abs(i-x[2])**2+abs(j-x[3])**2)
            route1=[[tasks[k][0],tasks[k][1],tasks[k][4]] for k in range(50)]
            route2=[[tasks[k][2],tasks[k][3],tasks[k][4]] for k in range(50)]
            a0,b0,idx0=route1[0]
            c1,d1,idx1=route2[-1]
            sc=dist(400,400,a0,b0)+dist(c1,d1,400,400)
            for k in range(len(route1)-1):
                a1,b1,_=route1[k]
                a2,b2,_=route1[k+1]
                sc+=dist(a1,b1,a2,b2)
                c1,d1,_=route2[k]
                c2,d2,_=route2[k+1]
                sc+=dist(c1,d1,c2,d2)
            if sc<min_sc:
                min_sc=sc
                best_y=i
                best_x=j
    tasks.sort(key=lambda x:abs(best_y-x[0])**2+abs(best_x-x[1])**2+abs(best_y-x[2])**2+abs(best_x-x[3])**2)
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
        if loop%100==0 and time.time()-time0>1.2:
            break
        # まず隣接swap
        i1=random.randint(1,47)
        i2=random.randint(1,47)
        while i1==i2:
            i2=random.randint(1,47)
        if abs(i1-i2)>=2:
            a0,b0,idx0=route1[i1-1]
            a1,b1,idx1=route1[i1]
            a2,b2,idx2=route1[i1+1]
            a3,b3,idx3=route1[i2-1]
            a4,b4,idx4=route1[i2]
            a5,b5,idx5=route1[i2+1]
            # 差分
            delta=0
            delta-=dist(a0,b0,a1,b1)+dist(a1,b1,a2,b2)+dist(a3,b3,a4,b4)+dist(a4,b4,a5,b5)
            a1,b1,a4,b4=a4,b4,a1,b1
            delta+=dist(a0,b0,a1,b1)+dist(a1,b1,a2,b2)+dist(a3,b3,a4,b4)+dist(a4,b4,a5,b5)
            if delta<0:
                route1[i1],route1[i2]=route1[i2],route1[i1]
                min_dist+=delta
        else:
            a0,b0,idx0=route1[i1-1]
            a1,b1,idx1=route1[i1] # この二つ
            a2,b2,idx2=route1[i1+1] #
            a3,b3,idx3=route1[i1+2]
            # 差分
            delta=0
            delta-=dist(a0,b0,a1,b1)+dist(a2,b2,a3,b3)
            a1,b1,a2,b2=a2,b2,a1,b1
            delta+=dist(a0,b0,a1,b1)+dist(a2,b2,a3,b3)
            if delta<0:
                route1[i1],route1[i1+1]=route1[i1+1],route1[i1]
                min_dist+=delta
    if DEBUG:
        print(loop)
    loop=0
    while True:
        loop+=1
        if loop%100==0 and time.time()-time0>1.9:
            break
        # まず隣接swap
        i1=random.randint(1,47)
        i2=random.randint(1,47)
        while i1==i2:
            i2=random.randint(1,47)
        if abs(i1-i2)>=2:
            c0,d0,idx0=route2[i1-1]
            c1,d1,idx1=route2[i1]
            c2,d2,idx2=route2[i1+1]
            c3,d3,idx3=route2[i2-1]
            c4,d4,idx4=route2[i2]
            c5,d5,idx5=route2[i2+1]
            # 差分
            delta=0
            delta-=dist(c0,d0,c1,d1)+dist(c1,d1,c2,d2)+dist(c3,d3,c4,d4)+dist(c4,d4,c5,d5)
            c1,d1,c4,d4=c4,d4,c1,d1
            delta+=dist(c0,d0,c1,d1)+dist(c1,d1,c2,d2)+dist(c3,d3,c4,d4)+dist(c4,d4,c5,d5)
            if delta<0:
                route2[i1],route2[i2]=route2[i2],route2[i1]
                min_dist+=delta
        else:
            c0,d0,idx0=route2[i1-1]
            c1,d1,idx1=route2[i1] # この二つ
            c2,d2,idx2=route2[i1+1] #
            c3,d3,idx3=route2[i1+2]
            # 差分
            delta=0
            delta-=dist(c0,d0,c1,d1)+dist(c2,d2,c3,d3)
            c1,d1,c2,d2=c2,d2,c1,d1
            delta+=dist(c0,d0,c1,d1)+dist(c2,d2,c3,d3)
            if delta<0:
                route2[i1],route2[i1+1]=route2[i1+1],route2[i1]
                min_dist+=delta
    if DEBUG:
        print(loop)
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