import random
import argparse
import numpy as np
from helper import (CustomInt, generate_random_list, 
                    find_slope, generate_plot)

def split(s,v):
    """ Splits the list `s` into 3 smaller lists.

      Returns 3 lists: s_l, s_v and s_r such that
       * s_l contains all elements from `s` that are less than `v`.
       * s_v contains all elements from `s` that are equal to `v`.
       * s_r contains all elements from `s` that are greater than `v`.
      
    """
    s_l = []
    s_v = []
    s_r = []

    ##########
    # TODO:


    ##########

    return (s_l, s_v, s_r)


def find_kth_smallest(s, k, c):
    """ Finds the `k`-th smallest element from the list `s` 

      In this implementation, we will use the median of `c`
      randomly chosen elements from `s` as the pivot.
    """
    # 1. Choose a random pivot.
    if c == 1 or len(s) < c:
        # choose an element at random from `s`.
        v = random.choice(s)
    else:
        # sample `c` elements from `s`.
        candidate_v = random.sample(s, c)
        # find the median of those elements.
        v = find_kth_smallest(candidate_v, c/2, 1)

    ##########
    # TODO:
    
    kth_smallest = 0

    ##########

    return kth_smallest

def average_runtime(n, rep, p, c):
    """ Finds the average (and the standard deviation) number of
    comparisons performed by find_kth_smallest().

    Arg
    ===
     n : number of elements
     rep : number of repititions
     p : a specific percentile in [0,1]
     c : the c parameter for find_kth_smallest() 
    
    NOTE FOR CSE103:

    We've provided a method for counting the number of comparisons:
      * CustomInt.reset_compare_count()
      * CustomInt.get_compare_count()

    The following example shows how to get the number of comparisons
    of a single run.

     CustomInt.reset_compare_count()
     find_kth_smallest(s, k, c)
     num_compares = CustomInt.get_compare_count()

    """
    # Create a list of random number of size n
    s = generate_random_list(n)
    k = int(n*p)

    ##########
    # TODO: 
        
    avg = 0
    stdev = 0  

    ##########

    return avg, stdev

def main(c):
    rep = 500
    p = 0.5
    all_n = [10, 100, 500, 1000, 2000]

    avgs = []
    stdevs = []
    for n in all_n:
        avg, stdev = average_runtime(n, rep, p, c)
        print "%d %0.2f %0.2f"%(n, avg, stdev)
        avgs.append(avg)
        stdevs.append(stdev)

    print "The average running time is %0.2fn"%(find_slope(all_n, avgs))
    
    generate_plot(all_n, avgs, stdevs, "percentile_c_%d.png"%(c))
    
    return avgs, stdevs

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find k smallest')
    parser.add_argument('-c', type=int, required=True, 
                        help='sample size for pivot selection')

    args = parser.parse_args()
    main(args.c)
