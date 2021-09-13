# dayベースじゃなくて、query_baseで作り直してみる
# その日に取れる行動で優先順位をつけてstackをつけていく感じ
# 局所探索は上のaction_listを保持しておいて何とかするとか？
# moneyの計算部分がズレてるせいでうまく機械を増やせていない
# 少なくとも2,3個まではgreedyにやって潰したほうがいいかも(もしくは10手先とかまで読み切るか)
# TODO:終盤に2,3手でいけるところに対し取り逃しをする場合にスコアの減少が見られるから、そこを改善する
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
                    score+=v*calc_cnt2(pos_machine,mr,mc)
                    break
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
    day=0
    while day<T:
        did=False
        # できそうなアクションの列挙
        # 序盤はmachineふやす
        if day<=900 and len(pos_machine)<40 and money>=(len(pos_machine)+1)**3: # 増やせる->一番大きいのを探す
            max_val=-1
            max_r=0
            max_c=0
            for i in range(N):
                for j in range(N):
                    if (i,j) in pos_machine:continue
                    sc=calc_score(pos_machine|{(i,j)},pos_vege)
                    if max_val<sc:
                        max_val=sc
                        max_r=i
                        max_c=j
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
            day+=1
            continue
        # 二手までは確実にgreedyでよさそう
        if len(pos_machine)<=2:
            best_sc=-1
            best_ac=[]
            for pr,pc in pos_machine:
                for r in range(N):
                    for c in range(N):
                        if (r,c) in pos_machine-{(pr,pc)}:continue
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
            if did:
                money,pos_machine,pos_vege=harvest(money,pos_machine,pos_vege)
                day+=1
                continue
        # 分離しているものがあれば先にmergeする(初手からやるとループしがち、ある程度大きくなってきてから)
        pr,pc=list(pos_machine)[0]
        if calc_cnt2(pos_machine,pr,pc)!=len(pos_machine):
            min_cnt=1000
            max_cnt=-1
            min_r,min_c=-1,-1
            max_r,max_c=-1,-1
            for mr,mc in pos_machine:
                cnt_near=calc_cnt2(pos_machine,mr,mc)
                if cnt_near<min_cnt:
                    min_cnt=cnt_near
                    min_r,min_c=mr,mc
                if cnt_near>max_cnt:
                    max_cnt=cnt_near
                    max_r,max_c=mr,mc
            vis=set()
            vis.add((max_r,max_c))
            q=[[max_r,max_c]]
            while q:
                y,x=q.pop()
                for ny,nx in [[y-1,x],[y+1,x],[y,x-1],[y,x+1]]:
                    if not (0<=ny<N and 0<=nx<N):
                        continue
                    if (ny,nx) not in vis:
                        vis.add((ny,nx))
                    if (ny,nx) not in vis and (ny,nx) in pos:
                        vis.add((ny,nx))
                        q.append((ny,nx))
            vis-=pos_machine
            best_ac=[]
            if len(vis):
                best_sc=-1
                best_ac=[]
                for mr,mc in vis:
                    pos_machine2=(pos_machine-{(min_r,min_c)})|{(mr,mc)}
                    sc=calc_score(pos_machine2,pos_vege)
                    if sc>best_sc:
                        best_sc=sc
                        best_ac=[min_r,min_c,mr,mc]
            if len(best_ac)==4:
                pr,pc,r,c=best_ac
                act.append(best_ac)
                pos_machine.remove((pr,pc))
                pos_machine.add((r,c))
                did=True
        if did:
            money,pos_machine,pos_vege=harvest(money,pos_machine,pos_vege)
            day+=1
            continue
        # 増やせないときは次の収穫のscoreを増やす(移動する)
        best_sc=-1
        best_ac=[]
        candi=list(calc_candi(pos_machine))
        for pr,pc in pos_machine:
            for r,c in candi:
                if (r,c) in pos_machine:
                    continue
                pos_machine2=(pos_machine-{(pr,pc)})|{(r,c)}
                for s,e,v in pos_vege[r][c]:
                    if s<=day<=e:
                        sc=v*calc_cnt2(pos_machine2,r,c)
                        if sc>best_sc:
                            best_sc=sc
                            best_ac=[pr,pc,r,c]
                        break
        best_v=-1
        best_r=-1
        best_c=-1
        best_mr=-1
        best_mc=-1
        for r in range(N):
            for c in range(N):
                if (r,c) in pos_machine:continue
                min_dist=10**9
                min_mr=-1
                min_mc=-1
                for mr,mc in pos_machine:
                    dd=abs(mr-r)+abs(mc-c)
                    if dd<min_dist:
                        min_dist=dd
                        min_mr=mr
                        min_mc=mc
                if min_dist!=2 or min_mr==-1:
                    continue
                # この時点で二手
                for s,e,v in pos_vege[r][c]:
                    if s<=day+1<=e:
                        if v>best_v:
                            best_v=v
                            best_r=r
                            best_c=c
                            best_mr=min_mr
                            best_mc=min_mc
                        break
        if best_r>=0 and best_v*len(pos_machine)/2.5>best_sc: # この枝刈りがめちゃくちゃ効く
            tar2=[best_r,best_c]
            if best_r==best_mr:
                tar1=[best_r,(best_c+best_mc)//2]
            elif best_c==best_mc:
                tar1=[(best_r+best_mr)//2,best_c]
            else:
                dx=best_r-best_mr
                dy=best_c-best_mc
                if dx==1:
                    tar1=[best_mr+1,best_mc]
                else:
                    tar1=[best_mr-1,best_mc]
            pos_machine2=pos_machine-{(best_mr,best_mc)}

            not_split=set()
            for mr1,mc1 in pos_machine2:
                pos_machine3=pos_machine2-{(mr1,mc1)}
                pr,pc=list(pos_machine3)[0]
                if calc_cnt2(pos_machine3|{(best_mr,best_mc)},pr,pc)==len(pos_machine2):
                    not_split.add((mr1,mc1))
            for mr1,mc1 in not_split:
                pos_machine3=(pos_machine2-{(mr1,mc1)})|{(tar1[0],tar1[1])}
                for mr2,mc2 in not_split-{(mr1,mc1)}-{(tar1[0],tar1[1])}:
                    pos_machine4=(pos_machine3-{(mr2,mc2)})|{(tar2[0],tar2[1])}
                    sc=best_v*calc_cnt2(pos_machine4|{(best_mr,best_mc)},tar2[0],tar2[1])
                    if sc/2.5>best_sc:
                        best_sc=sc/2.5
                        best_ac=[[mr1,mc1,tar1[0],tar1[1]],[mr2,mc2,tar2[0],tar2[1]]]
        if len(best_ac)==4:
            pr,pc,r,c=best_ac
            act.append(best_ac)
            pos_machine.remove((pr,pc))
            pos_machine.add((r,c))
            did=True
        elif len(best_ac)==2:
            pr1,pc1,r1,c1=best_ac[0]
            pr2,pc2,r2,c2=best_ac[1]
            act.append(best_ac[0])
            pos_machine.remove((pr1,pc1))
            pos_machine.add((r1,c1))
            money,pos_machine,pos_vege=harvest(money,pos_machine,pos_vege)
            day+=1
            act.append(best_ac[1])
            pos_machine.remove((pr2,pc2))
            pos_machine.add((r2,c2))
            did=True
        # どうしてもやることがない時はpass(保険)
        if not did:
            act.append([-1])
            did=True
        money,pos_machine,pos_vege=harvest(money,pos_machine,pos_vege)
        day+=1
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