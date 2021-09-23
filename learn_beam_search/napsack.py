import random
N=10**5
W=10**5
T=10**6 # loop
w=[0]*N
v=[0]*N
BEAM=100 # beam幅
curr=[] # 現在の状態(価値、重さ)
for i in range(N):
    w[i]=random.randint(1,10**5)
    v[i]=random.randint(1,10**5)
curr.append([0,0])
for i in range(N):
    nxt=[]
    for pv,pw in curr:
        nxt.append([pv,pw])
        if pw+w[i]<=W:
            nxt.append([v[i]+pv,pw+w[i]])
    nxt.sort(reverse=True)
    nxt=nxt[:BEAM]
    curr=nxt[:]
print("weight:",curr[0][1],"score:",curr[0][0])