import time

def FUN():
    max=time.time()+3
    while True:
        count=3
        print("TEST",count)
        if time.time()>max:
            count=1
            return count




print(FUN())