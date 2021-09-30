import random
DEBUG=True
def generate():
    if DEBUG:
        N,M=50,500
        while True:
            A=[[-1]*N for i in range(N)]
            A[0][0]=0
            A[0][N-1]=1
            A[N-1][0]=2
            A[N-1][N-1]=3
            MIN_POINT=3
            MAX_POINT=10
            for color in range(4):
                num_base=random.randint(MIN_POINT,MAX_POINT)
                painted=0
                while painted<num_base:
                    y=random.randint(0,N-1)
                    x=random.randint(0,N-1)
                    if A[y][x]==-1:
                        A[y][x]=color
                        painted+=1
            queue=[]
            def add_queue(yy,xx):
                for ny,nx in [[yy-1,xx],[yy+1,xx],[yy,xx-1],[yy,xx+1]]:
                    if 0<=ny<N and 0<=nx<N:
                        queue.append([ny,nx,A[yy][xx]])
            for i in range(N):
                for j in range(N):
                    if A[i][j]!=-1:
                        add_queue(i,j)
            while queue:
                idx=random.randint(0,len(queue)-1)
                queue[idx],queue[-1]=queue[-1],queue[idx]
                t=queue.pop()
                if A[t[0]][t[1]]==-1:
                    A[t[0]][t[1]]=t[2]
                    add_queue(t[0],t[1])
            # 条件確認
            cnt=[0]*4
            for i in range(N):
                for j in range(N):
                    cnt[A[i][j]]+=1
            if all(cnt[i]>=(N*N)//6 for i in range(4)):
                break
    else:
        N,M=map(int,input().split())
        A=[list(map(int,input().split())) for i in range(N)]
    return N,M,A
def calc_score(act,A):
    C=[[-1]*N for i in range(N)]
    C[0][0]=0
    C[0][N-1]=1
    C[N-1][0]=2
    C[N-1][N-1]=3
    now_color=0
    now_time=M
    cnt=0
    for x in act:
        cnt+=1
        if len(x)!=1:
            sy,sx,dir=x
            if C[sy][sx]!=now_color:
                print("Start with different color",cnt)
                return -1
            if dir=="R":
                for j in range(1,6):
                    if sx+j<N:
                        C[sy][sx+j]=now_color
            elif dir=="L":
                for j in range(1,6):
                    if sx-j>=0:
                        C[sy][sx-j]=now_color
            elif dir=="D":
                for i in range(1,6):
                    if sy+i<N:
                        C[sy+i][sx]=now_color
            else:
                for i in range(1,6):
                    if sy-i>=0:
                        C[sy-i][sx]=now_color
        now_color+=1
        now_color%=4
        now_time+=1
    score=0
    for i in range(N):
        for j in range(N):
            if A[i][j]==C[i][j]:
                score+=1
    return score
# 赤0 青1 緑2 黄3
def solve(N,M,A):
    C=[[-1]*N for i in range(N)]
    C[0][0]=0
    C[0][N-1]=1
    C[N-1][0]=2
    C[N-1][N-1]=3
    Dir={"L":(0,-1),"R":(0,1),"U":(-1,0),"D":(1,0)}
    rep=0
    ans=[]
    def paint(y,x,dir):
        ans.append([y,x,dir])
        dy,dx=Dir[dir]
        for i in range(1,6):
            yy,xx=y+dy*i,x+dx*i
            if not (0<=xx<N and 0<=yy<N):
                continue
            C[y+dy*i][x+dx*i]=rep%4
    paint(0,0,"R")
    rep+=1
    paint(0,49,"L")
    rep+=1
    for i in range(8):
        paint(49-i*5,0,"U")
        rep+=1
        paint(49-i*5,49,"U")
        rep+=1
        paint(i*5,5,"D")
        rep+=1
        paint(i*5,49-5,"D")
        rep+=1
    for i in range(4):
        y3=44-i*11
        y4=43-i*11
        y1=5+i*11
        y2=6+i*11
        for j in range(8):
            paint(y3,j*5,"R")
            rep+=1
            paint(y4,49-j*5,"L")
            rep+=1
            paint(y1,j*5+5,"R")
            rep+=1
            paint(y2,49-j*5-5,"L")
            rep+=1
    def legal_actions(C):
        actions=[]
        for i in range(N):
            for j in range(N):
                if C[i][j]>=0:
                    actions.append([i,j,C[i][j]])
        return actions
    while rep<M:
        now_color=rep%4
        can_ac=legal_actions(C)
        best_ac=[]
        best_sc=-1
        for yy,xx,col in can_ac:
            if col!=now_color:
                continue
            # R
            sc_r=0
            for j in range(1,6):
                if xx+j>=N:
                    break
                if A[yy][xx+j]==col:
                    sc_r+=1
                if A[yy][xx+j]==C[yy][xx+j]:
                    sc_r-=1
            # L
            sc_l=0
            for j in range(1,6):
                if xx-j<0:
                    break
                if A[yy][xx-j]==col:
                    sc_l+=1
                if A[yy][xx-j]==C[yy][xx-j]:
                    sc_l-=1
            # U
            sc_u=0
            for i in range(1,6):
                if yy-i<0:
                    break
                if A[yy-i][xx]==col:
                    sc_u+=1
                if A[yy-i][xx]==C[yy-i][xx]:
                    sc_u-=1
            # D
            sc_d=0
            for i in range(1,6):
                if yy+i>=N:
                    break
                if A[yy+i][xx]==col:
                    sc_d+=1
                if A[yy+i][xx]==C[yy+i][xx]:
                    sc_d-=1
            candi=[["R",sc_r],["L",sc_l],["U",sc_u],["D",sc_d]]
            candi.sort(key=lambda x:-x[1]) # score高い順に採用
            dir,sc=candi[0]
            if sc>best_sc:
                best_sc=sc
                best_ac=[yy,xx,dir]
        if best_sc>=0:
            paint(best_ac[0],best_ac[1],best_ac[2])
        else:
            ans.append([-1])
        rep+=1
    return ans
N,M,A=generate()
ans=solve(N,M,A)
if DEBUG:
    f1=open("input_half4.txt","w")
    f1.write(str(N)+" "+str(M)+"\n")
    for x in A:
        f1.write(" ".join(map(str,x))+"\n")
    f1.close()
    f2=open("output_half4.txt","w")
    for x in ans:
        f2.write(" ".join(map(str,x))+"\n")
    f2.close()
    print("score:",calc_score(ans,A))
else:
    for x in ans:
        print(*x)