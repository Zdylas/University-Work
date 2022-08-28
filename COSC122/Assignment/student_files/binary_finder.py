""" Your docstring should go here
Along with your name and email address
"""
from utilities import read_dataset
import classes
from stats import StatCounter

def find_plate(stolen_list, sighted_plate):
    comparison = 0
    found = False
    while len(stolen_list) != 1:
        middle = int(round(len(stolen_list)/2))
        comparison += 1
        if stolen_list[middle] <= sighted_plate:
            stolen_list = stolen_list[middle:]
        else:
            stolen_list = stolen_list[0:middle]
    comparison += 1
    if stolen_list[0] == sighted_plate:
        found = True
    return found, comparison


def binary_simple_plate_finder(stolen_plates, sighted_plates):
    """ Takes two lists of NumberPlates, returns a list and an integer.
    You can assume the stolen list will be in ascending order.
    You must assume that the sighted list is unsorted.

    The returned list contains stolen number plates that were sighted,
    in the same order as they appeared in the sighted list.
    The integer is the number of NumberPlate comparisons that
    were made.

    You can assume that each input list contains only unique plates,
    ie, neither list will contain more than one copy of any given plate.
    This fact will be very helpful in some special cases - you should
    think about when you can stop searching.    

    Note: you shouldn't alter either of the provided lists and you
    shouldn't make copies of either provided list. 
    """
    result_list = []
    i = 0
    total_comparisons = 0
    # ---start student section---
    while i < len(sighted_plates) and len(result_list) < len(stolen_plates):
        found, comparisons = find_plate(stolen_plates, sighted_plates[i])
        total_comparisons += comparisons
        if found:
            result_list.append(sighted_plates[i])
        i += 1
    # ===end student section===
    
    return result_list, total_comparisons
    


# ------------------------------------------------
# Extra stuff for your personal testing regime
# You can leave this stuff out of your submission


def run_tests():
    filename = "test_data/testing.txt"
    stolen_list, sightings, sighted_stolen_list = read_dataset(filename)
    print(binary_simple_plate_finder(stolen_list, sightings))
    print(StatCounter.get_comparisons()) 
    






if __name__ == '__main__':
    # This won't run when your module is imported from.
    # Use run_tests to try out some of your own simple tests.

    run_tests()
