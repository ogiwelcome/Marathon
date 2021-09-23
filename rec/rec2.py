# dayベースじゃなくて、query_baseで作り直してみる
# その日に取れる行動で優先順位をつけてstackをつけていく感じ
# 局所探索は上のaction_listを保持しておいて何とかするとか？
# moneyの計算部分がズレてるせいでうまく機械を増やせていない
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
def calc_cnt2(pos,y,x):
    vis=set()
    vis.add((y,x))
    q=[[y,x]]
    while q:
        y,x=q.pop()
        for ny,nx in [[y-1,x],[y+1,x],[y,x-1],[y,x+1]]:
            if not (0<=ny<N and 0<=nx<N):
                continue
            if (ny,nx) not in vis and (ny,nx) in pos:
                vis.add((ny,nx))
                q.append((ny,nx))
    return len(vis)
def calc_candi(pos):
    candi=set()
    candi|=set(pos)
    for pr,pc in pos:
        for nr,nc in [[pr-1,pc],[pr+1,pc],[pr,pc-1],[pr,pc+1]]:
            if 0<=nr<N and 0<=nc<N:
                candi.add((nr,nc))
    return candi
def simulate_init(query):
    money=1
    pos_machine=set()
    pos_vege=[[set() for i in range(N)] for j in range(N)]
    for R,C,S,E,V in query:
        pos_vege[R][C].add((S,E,V))
    act=[]
    def calc_score(pos_machine,pos_vege):
        score=0
        for mr,mc in pos_machine:
            for s,e,v in pos_vege[mr][mc]:
                if s<=day<=e:
                    sc=v*calc_cnt2(pos_machine,mr,mc)
                    score+=sc
        return score
    def harvest(money,pos_machine,pos_vege):
        # 収穫
        for mr,mc in pos_machine:
            for s,e,v in pos_vege[mr][mc]:
                if s<=day<=e:
                    sc=v*calc_cnt2(pos_machine,mr,mc)
                    money+=sc
                    pos_vege[mr][mc].remove((s,e,v))
                    break
        # 過ぎたやつ消す
        for i in range(N):
            for j in range(N):
                ss=set()
                for s,e,v in pos_vege[i][j]:
                    if e<=day:
                        ss.add((s,e,v))
                pos_vege[i][j]-=ss
        return money,pos_machine,pos_vege
    for day in range(T):
        did=False
        # できそうなアクションの列挙
        # 序盤はmachineふやす
        if len(pos_machine)<40 and money>=(len(pos_machine)+1)**3: # 増やせる->一番大きいのを探す
            max_val=-1
            max_r=0
            max_c=0
            for i in range(N):
                for j in range(N):
                    if (i,j) in pos_machine:continue
                    for s,e,v in pos_vege[i][j]:
                        if s<=day<=e:
                            if max_val<v:
                                max_val=v
                                max_r=i
                                max_c=j
                            break
            if max_val>=0:
                act.append([max_r,max_c])
                money-=(len(pos_machine)+1)**3
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
            money,pos_machine,pos_vege=harvest(money,pos_machine,pos_vege)
            continue
        # 増やせないときは次の収穫のscoreを増やす(移動する)
        best_sc=-10**9
        best_ac=[]
        candi=list(calc_candi(pos_machine))
        for pr,pc in pos_machine:
            for r,c in candi:
                if (r,c) in pos_machine:
                  continue
                pos_machine2=(pos_machine-{(pr,pc)})|{(r,c)}
                sc=calc_score(pos_machine2,pos_vege)
                if sc>best_sc:
                    best_sc=sc
                    best_ac=[pr,pc,r,c]
                
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
        money,pos_machine,pos_vege=harvest(money,pos_machine,pos_vege)
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