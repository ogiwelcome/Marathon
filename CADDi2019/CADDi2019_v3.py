import random
DEBUG=True
def generate():
    if DEBUG:
        L=1000
        N=1000
        M=100000
        ball=[]
        for i in range(N):
            r=random.randint(1,200)
            p=random.randint(1,max(1,r*r*r//100))
            ball.append([r,p])
        pair=[]
        for i in range(M):
            a=random.randint(1,N)
            b=random.randint(1,N)
            while a==b:
                b=random.randint(1,N)
            if a>b:
                a,b=b,a
            c=ball[a-1][0]+ball[b-1][0]+random.randint(1,200)
            d=random.randint(1,2*ball[a-1][0]*ball[b-1][0])
            pair.append([a,b,c,d])
    else:
        L,N,M=map(int,input().split())
        ball=[list(map(int,input().split())) for i in range(N)]
        pair=[list(map(int,input().split())) for i in range(M)]
    return L,N,M,ball,pair
# ビームサーチが良さそう、体積あたりの性能を評価できるから
# pairをそのまま当てはめるのか？→これもビームサーチならある程度なんとかなるか？
def dist(x1,y1,z1,x2,y2,z2):
    return ( (x1-x2)**2+(y1-y2)**2+(z1-z2)**2 )**0.5
def solve(L,N,M,ball,pair):
    pair_dict={}
    pair.sort(key=lambda x:x[3])
    # 重複の処理を分けたくない+小さいので最後に更新するとバグる(ビームサーチ部分)
    for a,b,c,d in pair:
        pair_dict[(a-1,b-1)]=(c,d) # 重複あり得るかも
    ball_init=[ball[i][:] for i in range(N)]
    ball=[ball[i]+[i] for i in range(N)]
    ball.sort(key=lambda x:x[1],reverse=True)
    BEAM=50
    eps=0.001 #　誤差用
    cur=[]
    cur.append([0,[]])
    for i in range(N):
        r,p,idx1=ball[i]
        nxt=[]
        for sc,xyzi in cur:
            nxt.append([sc,xyzi])
            for rep in range(10): # ここのパラメータはいじれそう
                nx,ny,nz=[random.randint(r,L-r) for _ in range(3)]
                delta_sc=0 # pairによる加算分
                flg=True
                for x,y,z,idx2 in xyzi:
                    d=dist(x,y,z,nx,ny,nz)
                    # pairの判定
                    i1,i2=idx1,idx2
                    if i1>i2:
                        i1,i2=i2,i1
                    if (i1,i2) in pair_dict:
                        lim_c,lim_d=pair_dict[(i1,i2)]
                        if d-eps<=lim_c:
                            delta_sc+=lim_d

                    if d-eps<ball_init[idx2][0]+r:
                        flg=False
                        break
                if flg:
                    sc2=sc+p+delta_sc
                    # random入れることで若干悪い遷移も取れるようになる
                    nxt.append([sc2,xyzi+[[nx,ny,nz,idx1]]])
                    break
        nxt.sort(reverse=True)
        cur=nxt[:BEAM]
    best_sc,best_xyzi=cur[0]
    best_xyz=[]
    # debug用 ############
    if DEBUG:
        error=[]
        for x1,y1,z1,i1 in best_xyzi:
            for x2,y2,z2,i2 in best_xyzi:
                if x1==-1 or x2==-1 or (x1==x2 and y1==y2 and z1==z2):
                    continue
                r1=ball_init[i1][0]
                r2=ball_init[i2][0]
                d=dist(x1,y1,z1,x2,y2,z2)
                if d-eps<r1+r2:
                    error.append([i1,i2])
        print("Error size coverd",len(error))
        error2=[]
        for x1,y1,z1,i1 in best_xyzi:
            r1=ball_init[i1][0]
            if not (r1<=x1<=L-r1 and r1<=y1<=L-r1 and r1<=z1<=L-r1):
                error2.append(i1)
        print("Error size over",len(error2))
    #####################
    for i in range(N):
        for x,y,z,idx in best_xyzi:
            if i==idx:
                best_xyz.append([x,y,z])
                break
        else:
            best_xyz.append([-1,-1,-1])
    return best_sc,best_xyz
L,N,M,ball,pair=generate()
best_sc,best_xyz=solve(L,N,M,ball,pair)
if DEBUG:
    print("best_sc:",best_sc)
else:
    for x,y,z in best_xyz:
        print(x,y,z)