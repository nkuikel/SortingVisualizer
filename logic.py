
# Base class for sorting algorithms
type SortStep = tuple[list[int], int, list[int]]  # (array, sorted_boundary, highlighted_indices)

class SortAlgorithm:
    def __init__(self, data: list[int]):
        '''
        Initializes the main class for sorting algorithms
        '''
        self.data = data

    def sort(self) -> SortStep:
        '''
        Abstract function that will be implemented in subclasses
        
        This method, the subclass, will use a generator (`yield`) to provide intermediate sorting steps for visualization.
        
        Yields:
            tuple: A snapshot of the sorting process as (`list`, `int`, `list`).
                - The current state of `arr` after modifications.
                - Index of the last sorted element.
                - List of indices currently being manipulated.
        '''
        raise NotImplementedError
class InsertionSort(SortAlgorithm):
    def sort(self):
        '''
        Overrides the sort module of parent class to implement the insertion sort algorithm. 
        Uses yield statement to send data periodically for visualization.
        '''
        arr = self.data
        n = len(arr)

        for i in range(1, n):
            key = arr[i]
            j = i - 1

            # highlight the key we're about to insert
            yield arr.copy(), i-1, [i]

            # shift everything > key, but only show the final
            #    “shift + key inserted at j” snapshot
            while j >= 0 and arr[j] > key:
                arr[j+1] = arr[j]
                display = arr.copy()
                display[j] = key
                yield display, i-1, [j, j+1]
                j -= 1

            # commit the key into the real array
            arr[j+1] = key
            yield arr.copy(), i, [j+1]

        # fully sorted
        yield arr.copy(), n-1, []

# Bubble Sort implementation
class BubbleSort(SortAlgorithm):
    def sort(self):
        '''
        Overrides the sort module of parent class to implement the bubble sort algorithm. 
        Uses yield statement to send data periodically for visualization.
        '''
        arr = self.data
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                yield arr.copy(), n-i-1, [j, j+1]
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    yield arr.copy(), n-i-1, [j, j+1]
        yield arr.copy(), len(arr)-1, []

# Selection Sort implementation
class SelectionSort(SortAlgorithm):
    def sort(self):
        '''
        Overrides the sort module of parent class to implement the selection sort algorithm. 
        Uses yield statement to send data periodically for visualization.
        '''
        arr = self.data
        n = len(arr)
        for i in range(n):
            min_idx = i
            yield arr.copy(), i-1, [min_idx]
            for j in range(i+1, n):
                yield arr.copy(), i-1, [min_idx, j]
                if arr[j] < arr[min_idx]:
                    min_idx = j
                    yield arr.copy(), i-1, [min_idx]
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            yield arr.copy(), i, [i, min_idx]
        yield arr.copy(), n-1, []
