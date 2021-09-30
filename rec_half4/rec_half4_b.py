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
    for x in act:
        if len(x)!=1:
            sy,sx,dir=x
            if C[sy][sx]!=now_color:
                print("Start with different color")
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
    ans=[]
    def legal_actions(C):
        actions=[]
        for i in range(N):
            for j in range(N):
                if C[i][j]>=0:
                    actions.append([i,j,C[i][j]])
        return actions
    for rep in range(M):
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
                if C[yy][xx+j]==-1:
                    sc_r+=3
                if A[yy][xx+j]==col:
                    sc_r+=1
                if A[yy][xx+j]==C[yy][xx+j] and C[yy][xx+j]!=col:
                    sc_r-=1
            # L
            sc_l=0
            for j in range(1,6):
                if xx-j<0:
                    break
                if C[yy][xx-j]==-1:
                    sc_l+=3
                if A[yy][xx-j]==col:
                    sc_l+=1
                if A[yy][xx-j]==C[yy][xx-j] and C[yy][xx-j]!=col:
                    sc_l-=1
            # U
            sc_u=0
            for i in range(1,6):
                if yy-i<0:
                    break
                if C[yy-i][xx]==-1:
                    sc_u+=3
                if A[yy-i][xx]==col:
                    sc_u+=1
                if A[yy-i][xx]==C[yy-i][xx] and C[yy-i][xx]!=col:
                    sc_u-=1
            # D
            sc_d=0
            for i in range(1,6):
                if yy+i>=N:
                    break
                if C[yy+i][xx]==-1:
                    sc_d+=3
                if A[yy+i][xx]==col:
                    sc_d+=1
                if A[yy+i][xx]==C[yy+i][xx] and C[yy+i][xx]!=col:
                    sc_d-=1
            candi=[["R",sc_r],["L",sc_l],["U",sc_u],["D",sc_d]]
            candi.sort(key=lambda x:-x[1]) # score高い順に採用
            dir,sc=candi[0]
            if sc>best_sc:
                best_sc=sc
                best_ac=[yy,xx,dir]
        if best_sc>=0:
            ans.append(best_ac)
            yy,xx,dir=best_ac
            if dir=="R":
                for j in range(1,6):
                    if xx+j<N:
                        C[yy][xx+j]=now_color
            elif dir=="L":
                for j in range(1,6):
                    if xx-j>=0:
                        C[yy][xx-j]=now_color
            elif dir=="U":
                for i in range(1,6):
                    if yy-i>=0:
                        C[yy-i][xx]=now_color
            else:
                for i in range(1,6):
                    if yy+i<N:
                        C[yy+i][xx]=now_color
        else:
            ans.append([-1])
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