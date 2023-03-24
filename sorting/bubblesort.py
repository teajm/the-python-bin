def bubblesort(arr):
    n = len(arr)
    swapped = False
    #iterate through all elements
    for i in range(len(arr) - 1):
        for j in range (0,len(arr) - i - 1):
            
            #swap spots if  element is greater
            if (arr[j] > arr[j + 1]):
                swapped = True
                arr[j],arr[j+1] = arr[j+1],arr[j]
        if not swapped:
            return
    
def main():
    
    arr = [64, 34, 25, 12, 22, 11, 90]
    
    bubblesort(arr)
    print("Sorted array is:")
    for i in range(len(arr)):
        print("% d" % arr[i], end=" ")
        
if __name__ == '__main__':
    main()