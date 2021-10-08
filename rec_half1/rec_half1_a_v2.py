import random
DEBUG=True
def generate():
    if DEBUG:
        H,W,K=50,50,8
        s=[[random.randint(0,9) for j in range(W)] for i in range(H)]
    else:
        H,W,K=map(int,input().split())
        s=[list(input()) for i in range(H)]
        for i in range(H):
          for j in range(W):
            s[i][j]=int(s[i][j])
    return H,W,K,s
def gen_polyomino(n):
    if n==1:
        yield ((0,0),)
        return
    se=set(gen_polyomino(n-1))
    dydx=((1,0),(0,1),(-1,0),(0,-1))
    for p in se:
        me=set(p)
        for y,x in p:
            for dy,dx in dydx:
                nynx=(y+dy,x+dx)
                if nynx in me:
                    continue
                q=p+(nynx,)
                min_y=min(y for y,x in q)
                min_x=min(x for y,x in q)
                q=((y-min_y,x-min_x) for y,x in q)
                q=tuple(sorted(q))
                yield q
def solve(H,W,K,s):
    minos=list(set(gen_polyomino(K)))
    T=len(minos)
    candi=[]
    for y in range(H):
        for x in range(W):
            for t in range(T):
                val=1
                for k in range(K):
                    dy,dx=minos[t][k]
                    ny,nx=y+dy,x+dx
                    if not (0<=ny<H and 0<=nx<W):
                        val=0
                        break
                    val*=s[ny][nx]
                if val:
                    candi.append([y,x,t,val])
    candi.sort(key=lambda x:-x[3])
    vis=[[0]*W for i in range(H)]
    pieces=[]
    score=0
    for sy,sx,t,val in candi:
        flg=True
        for k in range(K):
            dy,dx=minos[t][k]
            ny,nx=sy+dy,sx+dx
            if vis[ny][nx]==1:
                flg=False
                break
        if flg:
            score+=val
            for k in range(K):
                dy,dx=minos[t][k]
                pieces.append([sy+dy,sx+dx])
                vis[sy+dy][sx+dx]=1
    return score,pieces
H,W,K,s=generate()
score,pieces=solve(H,W,K,s)
if DEBUG:
    f1=open("input_rec_half1_a.txt","w")
    f1.write(str(H)+" "+str(W)+" "+str(K)+"\n")
    for x in s:
        f1.write("".join(map(str,x))+"\n")
    f1.close()
    f2=open("output_rec_half1_a.txt","w")
    f2.write(str(len(pieces)//K)+"\n")
    for y,x in pieces:
        f2.write(str(y+1)+" "+str(x+1)+"\n")
    f2.close()
    print("score:",score)
else:
    print(len(pieces)//8)
    for y,x in pieces:
        print(y+1,x+1)