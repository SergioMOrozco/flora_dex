import time
from distributed import Client, LocalCluster,as_completed, fire_and_forget

def complex():
    time.sleep(10)
    print("complex")
    return 'complex'

def hard():
    time.sleep(5)
    print("hard")
    return 'hard'

def easy():
    time.sleep(1)
    print("easy")
    return 'easy'

def task(x):
    time.sleep(x)
    print(f"Task took: {x} seconds")
    return x

if __name__ == "__main__":
    cluster = LocalCluster()
    client = Client(cluster)

    futures = []

    # submit task to the client.
    for i in range(1):
        # distributed by default creates key from name of function and a hash that is generated
        f3 = client.submit(complex, key=f"{complex.__name__}{i}")
        futures.append(f3)
        f2 = client.submit(hard, key=f"{hard.__name__}{i}")
        futures.append(f2)
        f1 = client.submit(easy, priority=10,  key=f"{easy.__name__}{i}")

        ## ensures task is executed at least once
        fire_and_forget(f1)
        #futures.append(f1)
    completed = as_completed(futures)

    # we must wait for  the future to complete.
    for i in completed:
        i.result()

    
    futures = client.map(task,range(10))
    client.gather(futureshuffle 