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
# 普通にBFSじゃいかんのか？
# 0は絶対に踏めない
# 局所改善思いつけなさそう
def solve(H,W,K,s):
    vis=[[0]*W for i in range(H)]
    pieces=[]
    for lim in range(0,10)[::-1]:
        for i in range(H):
            for j in range(W):
                if vis[i][j]==1 or s[i][j]<=lim:
                    continue
                q=[[i,j]] # ここを開始時点でスタート
                piece=[[i,j]]
                vis[i][j]=1
                while q:
                    if len(piece)==8:
                        break
                    y,x=q.pop()
                    for ny,nx in [[y-1,x],[y+1,x],[y,x-1],[y,x+1]]:
                        if not (0<=ny<H and 0<=nx<W):
                            continue
                        if vis[ny][nx]==1 or s[ny][nx]<=lim:
                            continue
                        if len(piece)<8:
                            piece.append([ny,nx])
                            vis[ny][nx]=1
                            q.append([ny,nx])
                        else:
                            break
                if len(piece)==8:
                    pieces.extend(piece)
                else:
                    for y,x in piece:
                        vis[y][x]=0
    return pieces
H,W,K,s=generate()
pieces=solve(H,W,K,s)
#pieces.sort()
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
    print(len(pieces)//K)
else:
    print(len(pieces)//K)
    for y,x in pieces:
        print(y+1,x+1)