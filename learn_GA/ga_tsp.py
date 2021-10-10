# 二次元gridにおけるTSP(巡回セールスマン問題)について考察する
# とりあえずgeneratorは(y,x)形式でN Nodeを指定
# 最短経路は直線でOK(平行移動にはしない)
import random
def generate():
    N=50
    p=set()
    for _ in range(N):
        y,x=[random.randint(0,N-1) for i in range(2)]
        while (y,x) in p:
            y,x=[random.randint(0,N-1) for i in range(2)]
        p.add((y,x))
    p=list(p)
    return N,p
def generate_init_genes(num_individual, num_cnt):
    genes=[[0]*num_cnt for i in range(num_individual)]
    for i in range(num_individual):
        genes[i]=random.sample(range(num_cnt),k=num_cnt)
    return genes
def dist(y1,x1,y2,x2):
    return ( (x1-x2)**2+(y1-y2)**2 )**0.5
N,p=generate()
num_individual=15
# print(generate_init_genes(num_individual,N))
# 評価関数
def genes_path_l(genes, p):
    path_l=[0]*len(genes)
    for i in range(len(genes)):
        d=0
        for j in range(len(p)-1):
            y1,x1=p[genes[i][j]]
            y2,x2=p[genes[i][j+1]]
            d+=dist(y1,x1,y2,x2)
        path_l[i]=d
    return path_l
def generate_roulette(fitness): # fitness: vec
    tot=sum(fitness)
    roulette=[0]*len(fitness)
    for i in range(len(fitness)):
        roulette[i]=fitness[i]/tot
    return roulette
"""
N,cities=generate()
genes=generate_init_genes(3,N)
path_l=genes_path_l(genes,cities)
inv_path_l=[1/path_l[i] for i in range(len(path_l))]
print(path_l)
"""
def roulette_choice(fitness):
    roulette=generate_roulette(fitness)
    choiced=