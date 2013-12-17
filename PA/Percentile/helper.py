import random
import numpy as np

class CustomInt(object):
    """A custom integer class
     
      This class keeps track of the number of comparisons done on the
      instances of the class.
    """
    
    compare_count_ = 0
    
    @staticmethod
    def reset_compare_count():
        CustomInt.compare_count_ = 0
    
    @staticmethod
    def get_compare_count():
        return CustomInt.compare_count_
    
    def __init__(self, val=None, max_val=10000):
        if val is None:
            self.val_ = random.randint(0, max_val)
        else:
            self.val_ = val
    
    def __gt__(self, other):
        CustomInt.compare_count_ += 1
        return (self.val_ > other.val_)
    
    def __lt__(self, other):
        CustomInt.compare_count_ += 1
        return (self.val_ < other.val_)
    
    def __ge__(self, other):
        CustomInt.compare_count_ += 1
        return (self.val_ >= other.val_)
    
    def __le__(self, other):
        CustomInt.compare_count_ += 1
        return (self.val_ <= other.val_)
    
    def __eq__(self, other):
        CustomInt.compare_count_ += 1
        return (self.val_ == other.val_)
    
    def __ne__(self, other):
        CustomInt.compare_count_ += 1
        return (self.val_ == other.val_)
    
    def __repr__(self):
        return "%d"%self.val_

def generate_random_list(n):
    """ Generates a list of random integers of length `n`. """
    return [CustomInt() for i in range(n)]

def find_slope(x,y):
    """ Fits a linear function to (x,y) and returns the slope """
    return np.polyfit(x,y,1)[0]

def generate_plot(n,avgs,stdevs,filename):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        plt.figure()
        plt.errorbar(n, avgs, yerr=stdevs, fmt='sb-', lw=2)
        plt.xlabel('N')
        plt.ylabel('number of comparisons')
        ax = plt.gca()
        ax.text(0.25, 0.75, "average running time = %0.2fn"%(find_slope(n, avgs)),
                horizontalalignment='left',
                verticalalignment='bottom',
                transform=ax.transAxes)
        border = np.max(n)*0.05
        plt.xlim((0, np.max(n)+border))
        plt.title(filename)
        plt.grid()
        plt.savefig(filename)
    except:
        pass
