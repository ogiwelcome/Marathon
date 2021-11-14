# 明らかにスコアが高すぎるので何らかの制約が足りていないか、処理が違っているか
# true duration の計算にpre_sを使っていたので過剰に適合するのはそれはそう
# pre_sとズレてたらrandom.shuffleなどでかわしたほうがいいかも
# 働ける奴がいっぱい働いたほうがいいんだよね、実労働もそう
# こういう時まずは適当に仕事割り振ってみて返ってくるスピード見るんだよね、わかる
# 途中でwork_cntをresetするのはあんまり意味なさそう
# dのsumとかでソートしてもおもろそう->だめそう
# dのaveとの差分でソート→だめ
# tasksの前処理したさある
import random
from heapq import heappop,heappush
import sys
DEBUG=True
INF=10**9
def generate():
    if DEBUG:
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
    # ->これはいらない
    need=[set() for i in range(N)]
    for u,v in uv:
        need[v-1].add(u-1)
    # 適当に初期の予想のsを組む
    # これ有効か？
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
    work_cnt=[0]*M
    d_sum=[sum(d[i]) for i in range(N)]
    tasks=[i for i in range(N)]
    pre_start_day=[0]*N
    while True:
        todays_list=[]
        humans=[i for i in range(M)]
        humans.sort(key=lambda x:-work_cnt[x])

        for i in humans:
            if human[i]>=0:
                continue
            # 予測した範囲のsから最善のhumanを選択
            best_task=-1
            min_predicted_days=INF
            for j in tasks:
                if len(need[j])>0:
                    continue
                if task_state[j]!=0:
                    continue
                if day<=1500:
                    best_task=j
                    break
                else:
                    weight=0
                    for k in range(K):
                        weight+=max(0,d[j][k]-s[i][k]) # ここ次第
                    if weight==0:
                        predicted_days_ij=1
                    else:
                        predicted_days_ij=max(1,weight+random.randint(-3,3))
                    if predicted_days_ij<min_predicted_days:
                        min_predicted_days=predicted_days_ij
                        best_task=j
            if best_task>=0:
                todays_list.append([i+1,best_task+1])
                # before->doing
                task_state[best_task]=1
                human[i]=best_task
                pre_start_day[best_task]=day
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
                work_cnt[hmn]+=1
                # pre_sの調整->序盤は精度が悪いから終盤のみ使う(多分)
                delta_day=day-pre_start_day[doing_tsk]
                weight=0
                for k in range(K):
                    weight+=max(0,d[doing_tsk][k]-pre_s[hmn][k])
                if weight==0:
                    predicted_delta_day=1
                else:
                    predicted_delta_day=max(1,weight+random.randint(-3,3))
                min_delta=abs(predicted_delta_day-delta_day)
                min_ss=pre_s[hmn][:]
                loop=0
                while loop<400:
                    loop+=1
                    ss=min_ss[:]
                    idx1=random.randint(0,K-1)
                    idx2=random.randint(0,K-1)
                    while idx1==idx2:
                        idx2=random.randint(0,K-1)
                    ss[idx1],ss[idx2]=ss[idx2],ss[idx1]
                    weight=0
                    for k in range(K):
                        weight+=max(0,d[doing_tsk][k]-pre_s[hmn][k])
                    if weight==0:
                        predicted_delta_day=1
                    else:
                        predicted_delta_day=max(1,weight+random.randint(-3,3))
                    new_predicted_delta_day=abs(predicted_delta_day-delta_day)
                    if new_predicted_delta_day<min_delta:
                        min_delta=new_predicted_delta_day
                        min_ss[idx1],min_ss[idx2]=min_ss[idx2],min_ss[idx1]
                pre_s[hmn]=min_ss[:]
                
                ###
            if cnt_end==N:
                score_sum+=N+1999-day
                #print(sorted(work_cnt))
                return

            elif day==1999:
                score_sum+=cnt_end
                #print(sorted(work_cnt))
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
                    work_cnt[hmn]+=1
                    # pre_s
                    delta_day=day-pre_start_day[doing_tsk]
                    weight=0
                    for k in range(K):
                        weight+=max(0,d[doing_tsk][k]-pre_s[hmn][k])
                    if weight==0:
                        predicted_delta_day=1
                    else:
                        predicted_delta_day=max(1,weight+random.randint(-3,3))
                    min_delta=abs(predicted_delta_day-delta_day)
                    min_ss=pre_s[hmn][:]
                    loop=0
                    while loop<400:
                        loop+=1
                        ss=min_ss[:]
                        idx1=random.randint(0,K-1)
                        idx2=random.randint(0,K-1)
                        while idx1==idx2:
                            idx2=random.randint(0,K-1)
                        ss[idx1],ss[idx2]=ss[idx2],ss[idx1]
                        weight=0
                        for k in range(K):
                            weight+=max(0,d[doing_tsk][k]-pre_s[hmn][k])
                        if weight==0:
                            predicted_delta_day=1
                        else:
                            predicted_delta_day=max(1,weight+random.randint(-3,3))
                        new_predicted_delta_day=abs(predicted_delta_day-delta_day)
                        if new_predicted_delta_day<min_delta:
                            min_delta=new_predicted_delta_day
                            min_ss[idx1],min_ss[idx2]=min_ss[idx2],min_ss[idx1]
                    pre_s[hmn]=min_ss[:]
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