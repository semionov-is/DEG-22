#cli version
import sys 

prev = None
count = 0

for i, line in enumerate(sys.stdin):
    word, one = line.strip().split(',')
    one = int(one)

    if prev:
        if prev == word:
            count += one
        else:
            print(f'{prev},{count}')
            count = one
            prev = word
    else:
        prev = word
        count = one

print(f'{prev},{count}')
