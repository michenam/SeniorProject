with open('arts-select.txt', 'r') as f:
    for count, line in enumerate(f, start=1):
        if count % 10 == 0:
            print(line)