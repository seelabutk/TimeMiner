# Calculate the simple moving average for the given data
def sma(data, window):
    offset = (window - 1) / 2
    length = len(data)
    
    # Pad the front of the array so it will be graphed correctly
    result = [0 for i in range(offset)]
    partial_sum = 0
    
    # Calculate averages
    for i in range(offset, length-offset):
        # Left side, centerpoint, and right side sums
        partial_sum += sum([data[i - left] for left in range(1, offset + 1)])
        partial_sum += data[i]
        partial_sum +=sum([data[i + right] for right in range(1, offset + 1)])
        # Take average
        avg = partial_sum / window
        result.append(avg)
        partial_sum = 0

    # Pad the end of the array
    for i in range(offset):
        result.append(0)
    return result


def prepare():
    views = []
    for month in range(1,12):
        f = open('../views/2014-' + str(month).zfill(2) + '.txt')
        contents = f.read()
        contents = contents.splitlines()
        str_views = contents[1::2]
        split_views = [i.split() for i in str_views]

        page_views = []
        for line, lst in enumerate(split_views):
            page_views.append([])
            for j in lst:
                page_views[line].append(int(j))

        for i in range(len(page_views)):
            try:
                views[i] += page_views[i]
            except:
                views.append(page_views[i])

    results = []
    maximum = max([len(v) for v in views])
    for v in views:
        n = len(v)
        if n < maximum:
            results.append(sma(v + [0 for f in range(maximum - n)], 24))
        else:
            results.append(sma(v, 24))

    return results

if __name__=='__main__':
    prepare()
