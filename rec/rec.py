# dayベースじゃなくて、query_baseで作り直してみる
# その日に取れる行動で優先順位をつけてstackをつけていく感じ
# 局所探索は上のaction_listを保持しておいて何とかするとか？
import io,os
input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline
import random
from math import floor
import time
DEBUG=True
if DEBUG:
    N=16
    M=5000
    T=1000
    query=[]
    pos=[[[] for _ in range(N)] for __ in range(N)]
    for i in range(M):
        while True:
            l=random.randint(0,20)
            S=random.randint(0,T-1-l)
            E=S+l
            R=random.randint(0,N-1)
            C=random.randint(0,N-1)
            if all(map(lambda v:v[1]<S or E<v[0],pos[R][C])):
                v=random.uniform(0,1+S/100)
                V=floor(2**v)
                query.append([R,C,S,E,V])
                pos[R][C].append([S,E])
                break
    query.sort(key=lambda x:(x[2],x[0],x[1]))
else:
    N,M,T=map(int,input().split())
    query=[list(map(int,input().split())) for i in range(M)]
def calc_cnt(pos,y,x):
    pos=list(pos)
    flg=[0]*len(pos)
    for j in range(len(pos)):
        if pos[j][0]==y and pos[j][1]==x:
            flg[j]=1
            break
    q=[[y,x]]
    while q:
        y,x=q.pop()
        for ny,nx in [[y-1,x],[y+1,x],[y,x-1],[y,x+1]]:
            if not (0<=ny<N and 0<=nx<N):
                continue
            for j in range(len(pos)):
                if ny==pos[j][0] and nx==pos[j][1] and flg[j]==0:
                    flg[j]=1
                    q.append([ny,nx])
                    break
    return sum(flg)
def duplicate(y,x,pos):
    flg=False
    for ny,nx in pos:
      if ny==y and nx==x:
        flg=True
    return flg
def simulate_init(query):
    money=1
    pos_machine=set()
    pos_vege=[[set() for i in range(N)] for j in range(N)]
    for R,C,S,E,V in query:
        pos_vege[R][C].add((S,E,V))
    act=[]
    for day in range(T):
        did=False
        # できそうなアクションの列挙
        # 序盤はmachineふやす
        if day<=700 and money>=(len(pos_machine)+1)**3: # 増やせる->一番大きいのを探す
            max_val=-1
            max_r=0
            max_c=0
            for R,C,S,E,V in query:
                if (R,C) in pos_machine:
                    continue
                if S<=day<=E:
                    if max_val<V:
                        max_val=V
                        max_r=R
                        max_c=C
            if max_val>=0:
                money-=(len(pos_machine)+1)**3
                act.append([max_r,max_c])
                pos_machine.add((max_r,max_c))
                did=True
            else:
                for i in range(N):
                    for j in range(N):
                        if (not did) and ((i,j) not in pos_machine):
                            did=True
                            money-=(len(pos_machine)+1)**3
                            pos_machine.add((i,j))
                            act.append([i,j])
                            break
                    if did:
                        break
        if did:
            continue
        # 増やせないときは次の収穫のscoreを増やす(移動する)
        best_d_val=-10**9
        best_ac=[]
        for r in range(N):
            for c in range(N):
                if (r,c) in pos_machine:
                    continue
                for s,e,v in pos_vege[r][c]:
                    if s<=day<=e:
                        for pr,pc in pos_machine:
                            sc=v*calc_cnt(pos_machine-{(pr,pc)},r,c)
                            if sc>best_d_val:
                                best_d_val=sc
                                best_ac=[pr,pc,r,c]
        # 近くに寄せる場合
        for pr,pc in pos_machine:
            for nr,nc in pos_machine:
                if (pr,pc)==(nr,nc):continue
                d_sc=0
                q=[[nr,nc]]
                vis=set()
                nxt_r=-1
                nxt_c=-1
                while q:
                    y,x=q.pop()
                    for ny,nx in [[y-1,x],[y+1,x],[y,x-1],[y,x+1]]:
                        if (ny,nx) in vis:
                            continue
                        if not (0<=ny<N and 0<=nx<N):
                            continue
                        if not (ny,nx) in pos_machine:
                            nxt_r=ny
                            nxt_c=nx
                            break
                    if nxt_r>=0:
                        break
                if nxt_r>=0:
                    for s,e,v in pos_vege[nr][nc]:
                        if s<=day<=e:
                            d_sc+=v*calc_cnt((pos_machine-{(pr,pc)})|{(nxt_r,nxt_c)},nr,nc)
                            break
                    for s,e,v in pos_vege[nr][nc]:
                        if s<=day<=e:
                            d_sc-=v*calc_cnt((pos_machine-{(pr,pc)})|{(nxt_r,nxt_c)},pr,pc)
                    if d_sc>best_d_val:
                        best_d_val=d_sc
                        best_ac=[pr,pc,nxt_r,nxt_c]
        if len(best_ac)==4:
            pr,pc,r,c=best_ac
            act.append(best_ac)
            pos_machine.remove((pr,pc))
            pos_machine.add((r,c))
            did=True
        # どうしてもやることがない時はpass(保険)
        if not did:
            act.append([-1])
            did=True
        # 収穫
        for mr,mc in pos_machine:
            for s,e,v in pos_vege[mr][mc]:
                if s<=day<=e:
                    sc=v*calc_cnt(pos_machine,mr,mc)
                    money+=sc
                    pos_vege[mr][mc].remove((s,e,v))
                    break
    return money,act
money,ans_act=simulate_init(query)
if DEBUG:
    f1=open("input.txt","w")
    f1.write(str(N)+" "+str(M)+" "+str(T)+"\n")
    for x in query:
        f1.write(" ".join(map(str,x))+"\n")
    f1.close()
    f2=open("output.txt","w")
    for x in ans_act:
        f2.write(" ".join(map(str,x))+"\n")
    f2.close()
    print("action:",len(ans_act))
    print("money:",money)
else:
    for s in ans_act:
        print(*s)