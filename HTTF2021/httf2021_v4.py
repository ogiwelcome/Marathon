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
                print("No have")
                return -1
            for j in range(len(p)):
                x,y,idx=p[j]
                if x==nx and y==ny and idx!=-1:
                    print("Already exist")
                    return -1
                elif x==nx and y==ny:
                    p[j][2]=have.pop()
                    break
            else:
                p.append([nx,ny,have.pop()])
    if len(have)==100:
        return 4000-cnt
    else:
        print("too small, size:",len(have))
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
    not_use=[]
    use=[]
    for x,y,idx in p:
        if 0<=x<=9 and 0<=y<=9:
            not_use.append([x,y,idx])
        else:
            use.append([x,y,idx])
    p=[[0,0,-2]]+use[:]
    pos=[[] for i in range(100)]
    vis={}
    for x,y,idx in not_use:
        pos[idx]=[x,y]
        vis[(x,y)]=idx
    iter=1
    for i in range(10):
        if i%2:
            for j in range(10)[::-1]:
                if (i,j) in vis:
                    continue
                if iter<len(p):
                    pos[p[iter][2]]=[i,j]
                    iter+=1
        else:
            for j in range(10):
                if (i,j) in vis:
                    continue
                if iter<len(p):
                    pos[p[iter][2]]=[i,j]
                    iter+=1
    l=len(p)
    best_order=[p[i][:] for i in range(l)]
    while time.time()-time0<2.7:
        i=random.randint(1,l-2)
        j=random.randint(1,l-2)
        if i==j:continue
        if i>j:
            i,j=j,i
        delta=0
        x0,y0,i0=best_order[i-1]
        x1,y1,i1=best_order[i]
        x2,y2,i2=best_order[i+1]
        x3,y3,i3=best_order[j-1]
        x4,y4,i4=best_order[j]
        x5,y5,i5=best_order[j+1]
        if not (1<=i1<=98 and 1<=i4<=98):
            continue
        px0,py0=pos[i1-1]
        px1,py1=pos[i1]
        px2,py2=pos[i1+1]
        px3,py3=pos[i4-1]
        px4,py4=pos[i4]
        px5,py5=pos[i4+1]
        delta-=abs(x1-x0)+abs(y1-y0)
        delta-=abs(x2-x1)+abs(y2-y1)
        delta-=abs(x4-x3)+abs(y4-y3)
        delta-=abs(x5-x4)+abs(y5-y4)
        x1,y1,x4,y4=x4,y4,x1,y1
        delta+=abs(x1-x0)+abs(y1-y0)
        delta+=abs(x2-x1)+abs(y2-y1)
        delta+=abs(x4-x3)+abs(y4-y3)
        delta+=abs(x5-x4)+abs(y5-y4)
        # add
        delta-=abs(px1-px0)+abs(py1-py0)
        delta-=abs(px2-px1)+abs(py2-py1)
        delta-=abs(px4-px3)+abs(py4-py3)
        delta-=abs(px5-px4)+abs(py5-py4)
        px1,py1,px4,py4=px4,py4,px1,py1
        delta+=abs(px1-px0)+abs(py1-py0)
        delta+=abs(px2-px1)+abs(py2-py1)
        delta+=abs(px4-px3)+abs(py4-py3)
        delta+=abs(px5-px4)+abs(py5-py4)
        if delta<0:
            best_order[i],best_order[j]=best_order[j][:],best_order[i][:]
            pos[i1],pos[i4]=pos[i4][:],pos[i1][:]
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
    #print("expected:",100-len(vis),"calc:",len(idx_order))
    # 10×10に展開
    reorder=[[] for i in range(100)]
    iter=0
    for i in range(10):
        if i%2:
            for j in range(10)[::-1]:
                if (i,j) in vis:
                    num=vis[(i,j)]
                    reorder[num]=[i,j]
                else:
                    ans.append("O")
                    reorder[idx_order[iter]]=[i,j]
                    iter+=1
                if j!=0:
                    ans.append("L")
        else:
            for j in range(10):
                if (i,j) in vis:
                    num=vis[(i,j)]
                    reorder[num]=[i,j]
                else:
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
    for i in range(100-1):
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