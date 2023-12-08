#cli version
import sys 

header = sys.stdin.readline() 

for line in sys.stdin:
    words = line.strip().split(",")[0].split()

    for word in words:
        print(f"{word},1")
