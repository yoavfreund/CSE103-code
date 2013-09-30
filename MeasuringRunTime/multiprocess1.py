from multiprocessing import Process, Queue

def f(q,index):
    for i in range(1000000000):
        q.put([index,i])
        if i % 1000 == 0:
            print index,':',i

if __name__ == '__main__':
    p=[0]*4
    q=[0]*4
    for i in range(4):
        q[i] = Queue()
        p[i] = Process(target=f, args=(q[i],i,))
        p[i].start()

    try:
        for i in range(500):
            for j in range(4):
                q[j].get(timeout=1)
    except: pass

    for j in range(4):
        p[j].join()

    print "all done"
