arr = [2 , 1 , 8 , 5 , 3 , 45 , 42 , 29]


def quicksort(arr,low,high) :

    if (high - low == 0) :
        return
    pivot = arr[low] 
    p = low + 1 
    q = high - 1

    while p < q :
        if arr[p]  < arr[pivot] :
            p += 1
        if arr[q] > arr[pivot]  :
            q -= 1
        if arr[p] > arr[pivot] && arr[q] < arr[pivot] :
            temp = arr[p]
            arr[p] = arr[q]
            arr[q] = temp
    if q != pivot :
        temp = arr[pivot]
        arr[pivot] = arr[q]
        arr[q] = temp
    quicksort(arr,low,q-1)
    quicksort(arr,q+1,high)


quicksort(arr,0,len(arr))
print(arr)
    


