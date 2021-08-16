import sys
input=sys.stdin.readline
import random
import time
DEBUG=True
al=list("ABCDEFGH")
time0=time.time()
if DEBUG:
    N=20
    a=[[al[random.randint(0,len(al)-1)] for i in range(N)] for j in range(N)]
    L=random.randint(4,10)
    M=random.randint(400,800)
    s=[]
    for _ in range(M):
        y=random.randint(0,N-1)
        x=random.randint(0,N-1)
        d=random.randint(0,1)
        k=random.randint(L-2,L+2)
        if d==0:
            ss=[]
            for j in range(k):
                ss.append(a[y][(x+j)%N])
            s.append("".join(ss))
        else:
            ss=[]
            for i in range(k):
                ss.append(a[(y+i)%N][x])
            s.append("".join(ss))
else:
    N,M=map(int,input().split())
    s=[input().rstrip() for i in range(M)]
s_init=s[:] # scoring用
def erase(st):
    skip=[0]*len(s)
    for i in range(len(s)):
        for j in range(len(s)):
            if i!=j and s[i] in s[j]:
                skip[i]=1
                break
            elif i!=j and len(s[j])==20 and s[i] in s[j]*2:
                skip[i]=1
                break
    new_s=[]
    for i in range(len(s)):
        if not skip[i]:
            new_s.append(s[i])
    return new_s
def calc_score(arr):
    candi=[]
    for i in range(N):
        candi.append("".join(arr[i])*2)
    for i in range(N):
        tmp=[arr[j][i] for j in range(N)]
        candi.append("".join(tmp)*2)
    c=0
    for ss in s_init:
        for xx in candi:
            if ss in xx:
                c+=1
                break
    return round(c*10**8/M)
# 接続
def merge(st,candi):
    new_s=[]
    used=set()
    for l,i,j in candi:
        used.add(i)
        used.add(j)
        new_s.append(st[i]+st[j][l:])
    for z in range(len(st)):
        if z in used:continue
        new_s.append(st[z])
    return new_s
while time.time()-time0<2.0:
    s=erase(s)
    update=False
    for k in range(19,4,-1):
        use=set()
        merge_candi=[]
        for i in range(len(s)):
            for j in range(len(s)):
                if i==j:continue
                if i in use or j in use:continue
                if len(s[i])>=k and len(s[j])>=k and all(s[i][-z-1]==s[j][z] for z in range(k)):
                    merge_candi.append([k,i,j])
                    use.add(i)
                    use.add(j)
                    break
        if merge_candi:
            s=merge(s,merge_candi)
            update=True
            break
    if not update:
        break
M=len(s)
s.sort(key=lambda x:len(x),reverse=True)

# construct
s=s[:100]
sx=[] # ansのinit用
for i in range(len(s)):
    sx.append( s[i]+"."*(max(N-len(s[i]),0)) )
sd=[s[i]*2 for i in range(len(s))] # inの判定用
ave=0
for i in range(len(s)):
    ave+=len(s[i])
ave=ave//len(s)
use=[0]*len(s)
ans=[["."]*N for j in range(N)]
for i in range(N):
    max_idx=-1
    max_point=0
    max_cnt=-1
    for j in range(len(s)):
        if use[j]:continue
        if max_cnt==N:break
        for k in range(1,N): # split_point
            ans[i]=sx[j][k:]+sx[j][:k]
            cnt=0
            arr=[] # 列用
            for l in range(N):
                ss=[ans[t][l] for t in range(max(0,i-ave),i+1)]
                arr.append("".join(ss))
            for ss in arr:
                for m in range(len(s)):
                    if use[m]==1:continue
                    if ss in sd[m]:
                        cnt+=1
                        break
            if cnt>max_cnt:
                max_cnt=cnt
                max_idx=j
                max_point=k
                if max_cnt==N:break
    if max_cnt<=0: # ない場合は上から適当に埋める
        for j in range(len(s)):
            if use[j]==0:
                max_idx=j
                break
    ans[i]=list(sx[max_idx][max_point:]+sx[max_idx][:max_point])
    use[max_idx]=1
# 空いてるマスはほぼ意味ないから適当に埋める
for i in range(N):
    for j in range(N):
        if ans[i][j]==".":
            ans[i][j]=al[random.randint(0,len(al)-1)]
max_sc=calc_score(ans)
cnt_loop=0
u=0
print(calc_score(ans))
while time.time()-time0<2.8:
    cnt_loop+=1
    if cnt_loop%2:
        new_ans=[[ans[i][j] for j in range(N)] for i in range(N)]
        x=random.randint(0,N-1)
        y=random.randint(1,N-1)
        new_ans[x]=new_ans[x][y:]+new_ans[x][:y]
        n_sc=calc_score(new_ans)
        if n_sc>max_sc:
            max_sc=n_sc
            ans=[[new_ans[i][j] for j in range(N)] for i in range(N)]
    else:
        new_ans=[[ans[i][j] for j in range(N)] for i in range(N)]
        x=random.randint(0,N-1)
        y=random.randint(0,N-1)
        new_ans[x],new_ans[y]=new_ans[y],new_ans[x]
        n_sc=calc_score(new_ans)
        if n_sc>max_sc:
            max_sc=n_sc
            ans=[[new_ans[i][j] for j in range(N)] for i in range(N)]
#print(cnt_loop)
print(calc_score(ans))
for i in range(N):
    print("".join(ans[i]))