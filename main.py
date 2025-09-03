from gui import Visualizer # imports the visualizer class from the gui module
from logic import InsertionSort,BubbleSort,SelectionSort # imports sorting algorithm classes from the logic module

def main():
    '''It maps algorthms to their classes, create a visualizer instance, and start the menu.'''

#the block below creats a dictionary that maps algorithm names to their classes
    algos = {
        'Insertion Sort':InsertionSort,
        'Bubble Sort':BubbleSort,
        'Selection Sort':SelectionSort
            }
    
#the line below creates a visualizer instance and starts the menu loop with the algorithms
    Visualizer().menu_loop(algos)

#this block below runs the main() function when this file is executed
if __name__ == "__main__":
    main()
