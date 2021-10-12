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
def solve(N,K,A):
    ans=[]
    sa=[0]*N
    for i in range(N):
        sa[i]=A[i]-i-1
    for rep in range(K):
        MIN=min(sa)
        MAX=max(sa)
        if MAX<=0:
            break
        mi=sa.index(MIN)
        ma=sa.index(MAX)
        if N<mi+1+sa[mi]+MAX:
            MAX=N-(mi+1+sa[mi])
        ans.append([ma+1,ma+1,mi+1,mi+1,MAX])
        sa[ma]-=MAX
        sa[mi]+=MAX
    for i in range(N):
        sa[i]+=i+1
    return sa,ans
N,K,A=generate()
arr,ans=solve(N,K,A)
if DEBUG:
    print("calc_score:",calc_score(arr))
else:
    for x in ans:
        print(*x)