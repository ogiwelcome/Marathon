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
    tasks=[tasks[i]+[i+1] for i in range(N)]
    tasks.sort(key=lambda x:abs(400-x[0])+abs(400-x[1])+abs(400-x[2])+abs(400-x[3]))
    route=tasks[:50]
    route1=[[route[i][0],route[i][1],route[i][4]] for i in range(50)]
    route2=[[route[i][2],route[i][3],route[i][4]] for i in range(50)]
    route_idx=set([route[i][4] for i in range(len(route))])
    # 何番目かを管理
    route1_dict={}
    for i in range(50):
        a,b,idx=route1[i]
        route1_dict[(a,b,idx)]=i
    route2_dict={}
    for i in range(50):
        c,d,idx=route2[i]
        route2_dict[(c,d,idx)]=i
    task_dict={}
    for i in range(N):
        a,b,c,d,idx=tasks[i]
        task_dict[idx]=(a,b,c,d)
    #
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
    if DEBUG:
        print(min_dist)
    loop=0
    while True:
        loop+=1
        if loop%100==0 and time.time()-time0>0.8:
            break
        if loop%100==0:
            new_idx=random.randint(1,N)
            while new_idx in route_idx:
                new_idx=random.randint(1,N)
            swap1_idx=random.randint(1,48)
            a0,b0,idx0=route1[swap1_idx-1]
            a1,b1,idx1=route1[swap1_idx] # これを変える
            a2,b2,idx2=route1[swap1_idx+1]
            a1,b1,c1,d1=task_dict[idx1]
            swap2_idx=route2_dict[(c1,d1,idx1)]
            c3,d3,idx3=route2[swap2_idx-1]
            c4,d4,idx4=route2[swap2_idx] # これを変える
            c5,d5,idx5=route2[swap2_idx+1]
            na,nb,nc,nd=task_dict[new_idx]

            delta=0
            delta-=dist(a0,b0,a1,b1)+dist(a1,b1,a2,b2)+dist(c3,d3,c4,d4)+dist(c4,d4,c5,d5)
            delta+=dist(a0,b0,na,nb)+dist(na,nb,a2,b2)+dist(c3,d3,nc,nd)+dist(nc,nd,c5,d5)
            if delta<0:
                min_dist+=delta
                route1[swap1_idx]=(na,nb,new_idx)
                route2[swap2_idx]=(nc,nd,new_idx)
                route1_dict.pop((a1,b1,idx1))
                route1_dict[(na,nb,new_idx)]=swap1_idx
                route2_dict.pop((c4,d4,idx4))
                route2_dict[(nc,nd,new_idx)]=swap2_idx
                route_idx.remove(idx1)
                route_idx.add(new_idx)
            continue
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
    loop=0
    while True:
        loop+=1
        if loop%100==0 and time.time()-time0>1.6:
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
    route_idx=list(route_idx)
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