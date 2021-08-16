primes=[]
c=[0]*(10**7)
for i in range(2,10**7):
    if c[i]==0:
        for j in range(i,10**7,i):
            c[j]=i
for i in range(2,10**7):
    if c[i]==i:
        primes.append(i)
ans=[]
v=1
lim=10**9
for j in range(len(primes)):
    if v*primes[j]<=lim:
        v*=primes[j]
    else:
        ans.append(v)
        if len(ans)==100:
            break
        v=primes[j]
print(*ans,sep="\n")