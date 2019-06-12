
def getStart(filename):
    d = None
    with open(filename) as f:
        head = [next(f) for _ in range(4)]
        d = int(head[3][11:-2])
    return d


def writeResult(filename, result):
    import csv
    print(f'Write to{filename+".csv"}')
    with open(filename + '.csv', 'w') as f:
        writer = csv.writer(f)
        header = ['']+[t for t in range(60, 301, 30)]
        writer.writerow(header)
        for i in range(0, 10):
            row = [str(i+1)]+list(map(str, result[i]))
            writer.writerow(row)
    return 'a'