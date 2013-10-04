# A simple python script for calculating the probability that two people
# have the same birthday

days=365
P=1.0                           # the initial probability that there
                                # are no people with the same
                                # birthday, i.e. all birthdays are
                                # different
for i in range(days):           # i is the number of people
    P=P*(days-i)/days           # Multiply P by the probability that
                                # the i-th person does not land on any
                                # of the current birthdays
    print i,P
    if P<0.01: break
