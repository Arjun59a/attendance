arr = [ 99 , 45 , 93 , 52 , 53 ]


for i in range(0,len(arr)) :
    key = arr[i]
    j = i + 1 
    while j >= 0 && arr[j] > key :
        arr[j-1] = arr[j] 
        j += 1