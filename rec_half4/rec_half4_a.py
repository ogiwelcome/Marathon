import random
DEBUG=True
def generate():
    if DEBUG:
        N=1000
        W=8
        K=6
        V=8
        p=[]
        for i in range(N):
            c=random.randint(0,K-1)
            v=random.randint(1,V)
            p.append([c,v])
    else:
        N,W,K,V=map(int,input().split())
        p=[list(map(int,input().split())) for i in range(N)]
    return N,W,K,V,p
def calc_score(board):
    sc=0
    min_l=1<<30
    for i in range(len(board)):
        min_l=min(min_l,len(board[i]))
    for i in range(min_l):
        cnt=[0]*6
        for j in range(len(board)):
            cnt[board[j][i][0]]+=board[j][i][1]
        sc+=max(cnt)
    return sc
# 盤面は0を下として積み上げるイメージ
# できれば小手先の一手よりかは一発で最善手に近い手を考えられるようになりたい(ハーフだし)
# boardには(c,v)形式で保存
# 状態遷移を途中で抜き出せないようなものはビームサーチを試してみる価値あり
#　各段の色は最初に置かれたもので決め打ち
def solve(N,W,K,V,p):
    cur=[] # 現在の状態の保持
    BEAM=4 # ビーム幅
    cur.append([0,[[] for i in range(W)],[],[]])
    # cur-> (sc, board, action, each color)
    for ec,ev in p:
        nxt=[]
        for sc,board,ac,col in cur:
            lb=[len(board[i]) for i in range(W)]
            Mlb=max(lb)
            mlb=min(lb)
            for idx in range(W): # どこに加えるか
                if lb[idx]==Mlb: # 新たな段(色を固定する)
                    if Mlb-mlb>=10:
                        continue
                    col2=col+[ec]
                    sc2=sc+ev+random.randint(0,3) # 若干ランダムに
                    board2=[[[board[i][j][0],board[i][j][1]] for j in range(len(board[i]))] for i in range(W)]
                    board2[idx].append([ec,ev])
                    ac2=[ac[i] for i in range(len(ac))]+[idx]
                else:
                    height=len(board[idx])-1 # ずれ注意
                    sc2=sc+(ec==col[height])*ev+random.randint(0,3)
                    board2=[[[board[i][j][0],board[i][j][1]] for j in range(len(board[i]))] for i in range(W)]
                    board2[idx].append([ec,ev])
                    ac2=[ac[i] for i in range(len(ac))]+[idx]
                    col2=[col[i] for i in range(len(col))]
                nxt.append([sc2,board2,ac2,col2])
        nxt.sort(reverse=True)
        cur=nxt[:BEAM]
        #print(len(nxt))
    best_sc,best_board,best_ac,_=cur[0]
    return best_sc,best_board,best_ac
N,W,K,V,p=generate()
sc,board,ac=solve(N,W,K,V,p)
if DEBUG:
    print("score:",calc_score(board))
    for i in range(len(board)):
        print("col:",i,len(board[i]))
else:
    for col in ac:
        print(col)