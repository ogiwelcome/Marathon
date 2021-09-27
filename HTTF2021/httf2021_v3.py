import sys
input=sys.stdin.readline
import random
import time
DEBUG=True
time0=time.time()
def generate():
    if DEBUG:
        arr=[]
        N=20
        for i in range(N):
            for j in range(N):
                arr.append([i,j])
        random.shuffle(arr)
        pp=[arr[i][:] for i in range(100)]
        p=[pp[i]+[i] for i in range(100)]
    else:
        N=20
        pp=[list(map(int,input().split())) for i in range(100)]
        p=[pp[i]+[i] for i in range(100)]
    return N,p
def calc_score(path,p):
    nx,ny=0,0
    have=[]
    cnt=0
    for dd in path:
        if dd=="R":
            ny+=1
            cnt+=1
        elif dd=="L":
            ny-=1
            cnt+=1
        elif dd=="U":
            nx-=1
            cnt+=1
        elif dd=="D":
            nx+=1
            cnt+=1
        elif dd=="I":
            for j in range(len(p)):
                x,y,idx=p[j]
                if x==nx and y==ny and idx!=-1:
                    have.append(idx)
                    p[j][2]=-1
                    break
                elif x==nx and y==ny:
                    print("No exist")
                    return -1
        elif dd=="O":
            if not have:
                return -1
            for j in range(len(p)):
                x,y,idx=p[j]
                if x==nx and y==ny and idx!=-1:
                    return -1
                elif x==nx and y==ny:
                    p[j][2]=have.pop()
                    break
            else:
                p.append([nx,ny,have.pop()])
    if len(have)==100:
        return 4000-cnt
    else:
        return -1
def calc_path(px,py,x,y):
    res=[]
    dx=x-px
    dy=y-py
    if dx>0:
        for j in range(dx):
            res.append("D")
    else:
        for j in range(abs(dx)):
            res.append("U")
    if dy>0:
        for j in range(dy):
            res.append("R")
    else:
        for j in range(abs(dy)):
            res.append("L")
    return "".join(res)
def solve(N,p):
    p=[[0,0,-2]]+sorted(p,reverse=True)
    l=len(p)
    best_order=[p[i][:] for i in range(l)]
    while time.time()-time0<1.7:
        i=random.randint(1,99)
        j=random.randint(1,99)
        if i==j:continue
        if i>j:
            i,j=j,i
        if j-i==1: # 隣接
            delta=0
            x0,y0,_=best_order[i-1]
            x1,y1,_=best_order[i]
            x2,y2,_=best_order[j]
            x3,y3,_=best_order[j+1]
            delta-=abs(x1-x0)+abs(y1-y0)
            delta-=abs(x3-x2)+abs(y3-y2)
            delta+=abs(x2-x0)+abs(y2-y0)
            delta+=abs(x3-x1)+abs(y3-y1)
            if delta<0:
                best_order[i],best_order[j]=best_order[j][:],best_order[i][:]
        else:
            delta=0
            x0,y0,_=best_order[i-1]
            x1,y1,_=best_order[i]
            x2,y2,_=best_order[i+1]
            x3,y3,_=best_order[j-1]
            x4,y4,_=best_order[j]
            x5,y5,_=best_order[j+1]
            delta-=abs(x1-x0)+abs(y1-y0)
            delta-=abs(x2-x1)+abs(y2-y1)
            delta-=abs(x3-x2)+abs(y3-y2)
            delta-=abs(x4-x3)+abs(y4-y3)
            delta-=abs(x5-x4)+abs(y5-y4)
            x1,y1,x4,y4=x4,y4,x1,y1
            delta+=abs(x1-x0)+abs(y1-y0)
            delta+=abs(x2-x1)+abs(y2-y1)
            delta+=abs(x3-x2)+abs(y3-y2)
            delta+=abs(x4-x3)+abs(y4-y3)
            delta+=abs(x5-x4)+abs(y5-y4)
            if delta<0:
                best_order[i],best_order[j]=best_order[j][:],best_order[i][:]
    #print(best_order[:10])
    # ここから解を作る
    ans=[]
    for i in range(l-1):
        x1,y1,_=best_order[i]
        x2,y2,_=best_order[i+1]
        ans.append(calc_path(x1,y1,x2,y2))
        ans.append("I")
    #print(len("".join(ans)))
    ans.append(calc_path(best_order[-1][0],best_order[-1][1],0,0)) # 並べるために移動
    # この時点で最初に入れた(0,0)を切る(l=101->l=100)
    # ここまでで(0,0)に戻ってくる
    l-=1
    best_order=best_order[1:]
    idx_order=[best_order[i][2] for i in range(l)][::-1] # 上から入れるから
    # 10×10に展開
    reorder=[[] for i in range(l)]
    iter=0
    for i in range(10):
        if i%2:
            for j in range(10)[::-1]:
                ans.append("O")
                reorder[idx_order[iter]]=[i,j]
                iter+=1
                if j!=0:
                    ans.append("L")
        else:
            for j in range(10):
                ans.append("O")
                reorder[idx_order[iter]]=[i,j]
                iter+=1
                if j!=9:
                    ans.append("R")
        if i!=9:
            ans.append("D")
    # 展開したやつを順番に拾う
    ans.append(calc_path(i,j,reorder[0][0],reorder[0][1]))
    ans.append("I")
    for i in range(l-1):
        ans.append(calc_path(reorder[i][0],reorder[i][1],reorder[i+1][0],reorder[i+1][1]))
        ans.append("I")
    return "".join(ans)
N,P=generate()
ans=solve(N,P)
if DEBUG:
    f1=open("input_httf.txt","w")
    for x in P:
        f1.write(" ".join(map(str,x))+"\n")
    f1.close()
    f2=open("output_httf.txt","w")
    f2.write(ans)
    f2.close()
    print(calc_score(ans,P))
else:
    print(ans)