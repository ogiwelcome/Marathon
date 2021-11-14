# 明らかにスコアが高すぎるので何らかの制約が足りていないか、処理が違っているか
# true duration の計算にpre_sを使っていたので過剰に適合するのはそれはそう
# pre_sとズレてたらrandom.shuffleなどでかわしたほうがいいかも
import random
from heapq import heappop,heappush
import sys
DEBUG=True
INF=10**9
def generate():
    if DEBUG: # 本番はnumpyとpypyの関係で切ったほうがいい
        N,M,K,R=1000,20,random.randint(10,20),random.randint(1000,3000)
        d=[]
        for i in range(N):
            dd=[abs(random.gauss(0,1)) for j in range(K)]
            pi=random.uniform(10,40)/( sum([dd[j]**2 for j in range(K)])**0.5 )
            dd=[int(dd[j]*pi) for j in range(K)]
            d.append(dd)
        s=[]
        for i in range(M):
            ss=[abs(random.gauss(0,1)) for j in range(K)]
            pi=random.uniform(20,60)/( sum([ss[j]**2 for j in range(K)])**0.5 )
            ss=[int(ss[j]*pi) for j in range(K)]
            s.append(ss)
        uv=set()
        while len(uv)<R:
            h=random.randint(1,100)
            v=random.randint(h+1,N)
            u=v-h
            uv.add((u,v))
        uv=list(uv)
    else:
        N,M,K,R=map(int,input().split())
        d=[list(map(int,input().split())) for i in range(N)]
        uv=[list(map(int,input().split())) for i in range(R)]
        s=[]
        for i in range(M):
            ss=[abs(random.gauss(0,1)) for j in range(K)]
            pi=random.uniform(20,60)/( sum([ss[j]**2 for j in range(K)])**0.5 )
            ss=[int(ss[j]*pi) for j in range(K)]
            s.append(ss)
    return N,M,K,R,d,s,uv

def solve(N,M,K,R,d,s,uv):
    global score_sum
    # TODO:まず依存関係からorderを作る->トポロジカルソートでうまいことやる
    need=[set() for i in range(N)]
    for u,v in uv:
        need[v-1].add(u-1)
    # 適当に初期の予想のsを組む
    pre_s=[]
    for i in range(M):
        ss=[abs(random.gauss(0,1)) for j in range(K)]
        pi=random.uniform(20,60)/( sum([ss[j]**2 for j in range(K)])**0.5 )
        ss=[int(ss[j]*pi) for j in range(K)]
        pre_s.append(ss)
    task_state=[0]*N # 0->not start / 1->doing / 2->end
    human=[-1]*M # -1->not start / else->doing job id
    cnt_end=0 # for calc score
    true_end_human=[[] for i in range(2001)] # (task,human)
    day=0
    while True:
        todays_list=[]
        humans=[i for i in range(M)]
        for i in humans:
            if human[i]>=0:
                continue
            # 予測した範囲のsから最善のhumanを選択
            best_task=-1
            for j in range(N):
                if len(need[j])>0:
                    continue
                if task_state[j]!=0:
                    continue
                best_task=j
                break
            if best_task>=0:
                todays_list.append([i+1,best_task+1])
                # before->doing
                task_state[best_task]=1
                human[i]=best_task
                if DEBUG:
                    weight=0
                    for k in range(K):
                        weight+=max(0,d[best_task][k]-s[i][k])
                    if weight==0:
                        true_duration=1
                    else:
                        true_duration=max(1,weight+random.randint(-3,3))
                    true_end_human[min(2000,day+true_duration-1)].append(i)
        if DEBUG:
            for hmn in true_end_human[day]:
                doing_tsk=human[hmn]
                # doing->end
                task_state[doing_tsk]=2
                cnt_end+=1
                for nxt in range(doing_tsk+1,N):
                    if doing_tsk in need[nxt]:
                        need[nxt].remove(doing_tsk)
                human[hmn]=-1

            if cnt_end==N:
                score_sum+=N+1999-day
                return

            elif day==1999:
                score_sum+=cnt_end
                return
        else:
            arr=[len(todays_list)]
            for a,b in todays_list:
                arr+=[a,b] # ここのincrementが違ってた
            print(*arr)
            sys.stdout.flush()
            tmp=list(map(int,input().split()))
            if len(tmp)==1:
                if tmp[0]==-1:
                    exit()
                else:
                    pass
            else:
                for hmn in tmp[1:]:
                    hmn-=1
                    doing_tsk=human[hmn]
                    # doing->end
                    task_state[doing_tsk]=2
                    cnt_end+=1
                    for nxt in range(doing_tsk+1,N):
                        if doing_tsk in need[nxt]:
                            need[nxt].remove(doing_tsk)
                    human[hmn]=-1
        day+=1
if DEBUG:
    score_sum=0
    rep=100
    for _ in range(rep):
        N,M,K,R,d,s,uv=generate()
        solve(N,M,K,R,d,s,uv)
    score_sum/=rep
    print("average_score:",score_sum)
else:
    N,M,K,R,d,s,uv=generate()
    solve(N,M,K,R,d,s,uv)