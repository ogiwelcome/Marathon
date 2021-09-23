import random
import time
DEBUG=True
def generate():
    if DEBUG:
        N=40
        MAX_E=30
        E=[[0]*N for i in range(N)]
        prob=[0]+[1/(i*i) for i in range(1,MAX_E)]
        tot_prob=sum(prob)
        for i in range(N):
            for j in range(N):
                x=random.random()*tot_prob
                E[i][j]=x
                for k in range(1,MAX_E+1):
                    x-=prob[k]
                    if x<=0:
                        E[i][j]=k
                        break         
    else:
        N=int(input())
        E=[list(map(int,input().split())) for i in range(N)]
    return N,E
def calc_score(E,P):
    sc=0
    for i in range(N):
        for j in range(N):
            sc+=E[i][j]*P[i][j]
    return sc
def solve(N,E):
    time0=time.time()
    candi=[]
    for i in range(N):
        for j in range(N):
            candi.append([E[i][j],i,j])
    candi.sort(reverse=True)
    use=[]
    for _,y,x in candi:
        lim=50
        if len(use)>lim:
            break
        l=( lim-len(use) )//10+1
        flg=True
        for ll,yy,xx in use:
            if abs(yy-y)+abs(xx-x)<=max(ll,l):
                flg=False
                break
        if flg:
            use.append([l,y,x])
    loop=0
    while time.time()-time0<1.75:
        loop+=1
        if loop%5000==0 and len(use)>=2: # 壊す
            idx=random.randint(0,len(use)-1)
            l,y,x=use[idx]
            dx=random.randint(1,l)
            if l-dx==0:
                use=use[:idx]+use[idx+1:]
            else:
                use[idx]=[l-dx,y,x]
        if loop%50:
            idx=random.randint(0,len(use)-1)
            l,y,x=use[idx]
            dx=random.randint(1,5)
            if l+dx>N:
                continue

            l+=dx
            flg=True
            for j in range(len(use)):
                if j==idx:
                    continue
                ll,yy,xx=use[j]
                if abs(yy-y)+abs(xx-x)<=max(ll,l):
                    flg=False
                    break
            if flg:
                use[idx]=[l,y,x]
        else:
            y=random.randint(0,N-1)
            x=random.randint(0,N-1)
            l=1
            flg=True
            for ll,yy,xx in use:
                if yy==y and xx==x:
                    flg=False
                    break
                if abs(yy-y)+abs(xx-x)<=max(ll,l):
                    flg=False
                    break
            if flg:
                use.append([l,y,x])
    if DEBUG:
        print(len(use))
    P=[[0]*N for i in range(N)]
    for l,y,x in use:
        P[y][x]=l
    return P
########################################
N,E=generate()
P=solve(N,E)
if DEBUG:
    """
    f1=open("input.txt","w")
    f1.write(str(N)+"\n")
    for e in E:
        f1.write(" ".join(map(str,e))+"\n")
    f1.close()
    f2=open("output.txt","w")
    for p in P:
        f2.write(" ".join(map(str,p))+"\n")
    f2.close()
    """
    ans=calc_score(E,P)
    print("score:",ans)
else:
    for pp in P:
        print(*pp)