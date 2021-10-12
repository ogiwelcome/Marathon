import random
DEBUG=True
def generate():
    if DEBUG:
        N=30000
        K=random.randint(0,40)*50+1000
        A=[i for i in range(1,N+1)]
        random.shuffle(A)
    else:
        N,K=map(int,input().split())
        A=[int(input()) for i in range(N)]
    return N,K,A
def calc_score(A):
    sc=10**9
    N=len(A)
    for i in range(N):
        sc-=abs(i+1-A[i])
        if not 1<=A[i]<=N:
            return -1*A[i]
    return sc
# ビームサーチが雑に実装できて強そう
def solve(N,K,A):
    BEAM=4
    width=5 # 一度に変更する区間幅
    cur=[]
    cur.append([calc_score(A),A[:],[]]) # sc,changed_A,actions
    for rep in range(K):
        #print(rep,len(cur))
        nxt=[]
        for n_sc,n_A,n_ac in cur:
            for rep2 in range(6):
                l1=random.randint(0,N-width-1)
                r1=l1+width
                l2=random.randint(0,N-width-1)
                r2=l2+width
                if not (r1<l2 or r2<l1):
                    continue
                lim=N # vでどこまで取れるか
                for i in range(l1,r1+1):
                    lim=min(lim,n_A[i]-1)
                for i in range(l2,r2+1):
                    lim=min(lim,N-n_A[i]-1)
                if lim<=1:
                    continue
                v=random.randint(1,lim)
                c_A=n_A[:]
                delta=0
                for i in range(l1,r1+1):
                    delta+=abs(i+1-n_A[i])
                    c_A[i]-=v
                    delta-=abs(i+1-c_A[i])
                for i in range(l2,r2+1):
                    delta+=abs(i+1-n_A[i])
                    c_A[i]+=v
                    delta-=abs(i+1-c_A[i])
                nxt.append([n_sc+delta,c_A,n_ac+[[l1+1,r1+1,l2+1,r2+1,v]]])
        nxt.sort(reverse=True)
        cur=nxt[:BEAM]
    best_sc,best_A,best_ac=cur[0]
    return best_sc,best_A,best_ac
N,K,A=generate()
best_sc,best_A,best_ac=solve(N,K,A)
if DEBUG:
    print("best_sc:",best_sc)
    print("calc_sc:",calc_score(best_A))
else:
    for x in best_ac:
        print(*x)