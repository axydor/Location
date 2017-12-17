import os
from multiprocessing import Process

def worker(_file):
    os.system('python3 eventClient.py < '+_file)


Files = ["input1.txt", "input2.txt", "input3.txt"]

for f in Files:
    p = Process(target=worker, args=(f,))
    p.start()
