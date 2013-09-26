from random import random

def sample(n,m,p_true,p_empirical):
    """Generate m sequences of length n using a coin with bias p_true
    Count the number of sequences that contain exactly n*p_empir 1's

    """
    count=0
    for j in range(m):
        outcomes=[(1 if random()<p_true else 0) for i in range(n)]
        if sum(outcomes)==int(n*p_empirical): count += 1
    return count

k= 5        # number of repeats
n=1000       # length of sequence
m=1000      # number of samples

for i in range(k):
    count1=sample(n,m,0.2,0.1)
    count2=sample(n,m,0.2,0.2)
    if count2==0: count2=1
    print '%d,%d,%5.3f' % (count1,count2,(count1+0.0)/(count2+0.0))
