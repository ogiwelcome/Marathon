import sys
input=sys.stdin.readline
import random
import time
import math
from heapq import heappop,heappush
time0=time.time()
DEBUG=True
if DEBUG:
    D=365
    c=[random.randint(0,100) for i in range(26)]
    s=[[random.randint(0,20000) for j in range(26)] for i in range(D)]
else:
    D=int(input())
    c=list(map(int,input().split()))
    s=[list(map(int,input().split())) for i in range(D)]
def calc_score(arr):
    last=[0]*26
    sc=0
    for d in range(D):
        last[arr[d]]=d+1
        sc+=s[d][arr[d]]
        for i in range(26):
            sc-=c[i]*(d+1-last[i])
    return sc
# score関数は改良できる->scoreをそれぞれのtypeで分けておくことで
# swap操作前後で定数で遷移できる
def calc_score_init(arr):
    score=[0]*26
    days=[[] for i in range(26)]
    for i in range(len(arr)): # 0-indexed
        days[arr[i]].append(i)
    for i in range(26):
        for j in range(len(days[i])):
            score[i]+=s[days[i][j]][i]
        if days[i]:
            score[i]-=c[i]*days[i][0]*(days[i][0]+1)//2+c[i]*(D-1-days[i][-1])*(D-1-days[i][-1]-1)//2
        for j in range(len(days[i])-1):
            dx=days[i][j+1]-days[i][j]
            score[i]-=c[i]*dx*(dx-1)//2
    return score,days
# time周りの設定はここに書いておく
# T0:1回の遷移で動きうるスコア幅の最大値とか
# T1:1回の遷移で動きうるスコア幅の最小値とか
T0=2000;T1=600
time_lim=18
# 確率計算のタイミングでtimeを呼んでおり、これがボトルネックになりうる
# step数が決まっているなら予めrateを決めておくのも選択肢
def prob(now_t,delta_score):
    t_normalized=(time_lim+1-now_t)/time_lim
    T=(T0**(1-t_normalized))*(T1**t_normalized)
    if delta_score>=0:
        return 1
    else:
        try:
            return math.exp(delta_score/T)
        except:
            return 1
def calc_score_changed_type1_with_prob(arr,score_arr,days_arr,day_num,after):
    n_score=[score_arr[i] for i in range(len(score_arr))]
    n_days=[[days[i][j] for j in range(len(days[i]))] for i in range(26)]
    n_arr=[arr[i] for i in range(len(arr))]
    before=n_arr[day_num]
    n_arr[day_num]=after
    #print(n_days[before],day_num)
    #print(n_days[before-1])
    n_days[before].remove(day_num)
    n_days[after].append(day_num)
    n_days[after].sort()
    delta_before=0;delta_after=0
    for j in range(len(n_days[before])):
        delta_before+=s[n_days[before][j]][before]
    if n_days[before]:
        delta_before-=c[before]*n_days[before][0]*(n_days[before][0]+1)//2
        delta_before-=c[before]*(D-1-n_days[before][-1])*(D-1-n_days[before][-1]-1)//2
    for j in range(len(n_days[before])-1):
        dx=n_days[before][j+1]-n_days[before][j]
        delta_before-=c[before]*dx*(dx-1)//2
    for j in range(len(n_days[after])):
        delta_after+=s[n_days[after][j]][after]
    if n_days[after]:
        delta_after-=c[after]*n_days[after][0]*(n_days[after][0]+1)//2
        delta_after-=c[after]*(D-1-n_days[after][-1])*(D-1-n_days[after][-1]-1)//2
    for j in range(len(n_days[after])-1):
        dx=n_days[after][j+1]-n_days[after][j]
        delta_after-=c[after]*dx*(dx-1)//2
    u=random.random() # 一様乱数からとる
    delta_score=delta_before+delta_after-score_arr[before]-score_arr[after]
    pp=prob(time.time()-time0,delta_score)
    if pp>u:
        n_score[before]=delta_before
        n_score[after]=delta_after
        return n_score,n_days,n_arr
    else:
        return score_arr,days_arr,arr
def calc_score_changed_type2_with_prob(arr,score_arr,days_arr,day_num1,day_num2):
    n_score=[score_arr[i] for i in range(len(score_arr))]
    n_days=[[days[i][j] for j in range(len(days[i]))] for i in range(26)]
    n_arr=[arr[i] for i in range(len(arr))]
    before1=n_arr[day_num1]
    before2=n_arr[day_num2]
    n_arr[day_num1]=before2
    n_arr[day_num2]=before1
    #print(n_days[before],day_num)
    #print(n_days[before-1])
    n_days[before1].remove(day_num1)
    n_days[before2].remove(day_num2)
    n_days[before1].append(day_num2)
    n_days[before2].append(day_num1)
    n_days[before1].sort()
    n_days[before2].sort()
    delta_before1=0;delta_before2=0
    for j in range(len(n_days[before1])):
        delta_before1+=s[n_days[before1][j]][before1]
    if n_days[before1]:
        delta_before1-=c[before1]*n_days[before1][0]*(n_days[before1][0]+1)//2
        delta_before1-=c[before1]*(D-1-n_days[before1][-1])*(D-1-n_days[before1][-1]-1)//2
    for j in range(len(n_days[before1])-1):
        dx=n_days[before1][j+1]-n_days[before1][j]
        delta_before1-=c[before1]*dx*(dx-1)//2
    for j in range(len(n_days[before2])):
        delta_before2+=s[n_days[before2][j]][before2]
    if n_days[before2]:
        delta_before2-=c[before2]*n_days[before2][0]*(n_days[before2][0]+1)//2
        delta_before2-=c[before2]*(D-1-n_days[before2][-1])*(D-1-n_days[before2][-1]-1)//2
    for j in range(len(n_days[before2])-1):
        dx=n_days[before2][j+1]-n_days[before2][j]
        delta_before2-=c[before2]*dx*(dx-1)//2
    u=random.random() # 一様乱数からとる
    delta_score=delta_before1+delta_before2-score_arr[before1]-score_arr[before2]
    pp=prob(time.time()-time0,delta_score)
    if pp>u:
        n_score[before1]=delta_before1
        n_score[before2]=delta_before2
        return n_score,n_days,n_arr
    else:
        return score_arr,days_arr,arr
def estimate(arr,delay): # 1-indexed
    last=[0]*26
    sc=0
    for d in range(len(arr)):
        last[arr[d]]=d+1
        for i in range(26):
            sc-=(d+1-last[i])*c[i]
        sc+=s[d][arr[d]]
    for d in range(len(arr),min(len(arr)+delay,D)):
        for i in range(26):
            sc-=(d+1-last[i])*c[i]
    return sc
# out:適当な初期解->局所解にハマってないか確認しながら
out=[]
last=[0]*26
now_sc=0
delay=7
for i in range(D):
    best_idx=0
    max_sc=-10**9
    for j in range(26):
        out.append(j)
        sc=estimate(out,delay)
        if max_sc<sc:
            max_sc=sc
            best_idx=j
        out.pop()
    out.append(best_idx)
score,days=calc_score_init(out)
# 局所探索 /1点の変更と2点swapを交互に
flg=0 # ^を管理するやつ
print(calc_score(out))
cnt_loop=0
while True:
    cnt_loop+=1
    if cnt_loop%100==0:
        if time.time()-time0>time_lim:
            break
    flg+=1;flg%=2
    if flg:
        num=random.randint(0,D-1)
        after=random.randint(0,25)
        score,days,out=calc_score_changed_type1_with_prob(out,score,days,num,after)
    else:
        num1=random.randint(0,D-1)
        num2=random.randint(0,D-1)
        while num1==num2:
            num2=random.randint(0,D-1)
        score,days,out=calc_score_changed_type2_with_prob(out,score,days,num1,num2)
print(cnt_loop)
print(calc_score(out))
for i in range(len(out)):
    out[i]+=1
#print(*out,sep="\n")