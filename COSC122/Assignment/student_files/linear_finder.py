""" Your docstring should go here
Author = Dominic McNulty
Email = dmc274@uclive.ac.nz
"""

from utilities import read_dataset
import classes
from stats import StatCounter




def linear_simple_plate_finder(stolen_plates, sighted_plates):
    """
    Takes two lists of NumberPlates as input.
    Returns a list and an integer.

    The returned list contains stolen number plates that were sighted,
    in the same order as they appeared in the sighted list.
    The integer is the number of NumberPlate comparisons that
    were made.

    You cannot assume either list is sorted, ie, you should assume the
    lists are not sorted.

    You can assume that each input list contains only unique plates,
    ie, neither list will contain more than one copy of any given plate.
    This fact will be very helpful in some special cases - you should
    think about when you can stop searching.

    Note: you shouldn't alter either of the provided lists and you
    shouldn't make copies of either provided list. Such things would
    alter data or take extra time!
    """
    result_list = []
    i = 0
    total_comparisons = 0
    # ---start student section---
    while i < len(sighted_plates) and len(result_list) < len(stolen_plates):
        for plate in stolen_plates:
            total_comparisons += 1
            if sighted_plates[i] == plate:
                result_list.append(sighted_plates[i])
                break
        i += 1

    # ===end student section===
    return result_list, total_comparisons


# ------------------------------------------------
# Extra stuff for your personal testing regime
# You can leave this stuff out of your submission

def run_tests():
    """ Use this function to run some simple tests
    to help with developing your awesome answer code.
    You should leave this out of your submission """
    filename = "test_data/100s-1000-100-a.txt"
    stolen_list, sightings, sighted_stolen_list = read_dataset(filename)
    stolen_list = ['500000']
    sightings = ['600000']
    print(linear_simple_plate_finder(stolen_list, sightings))
    print(StatCounter.get_comparisons()) 
    



# You can leave the following out of your submission
if __name__ == '__main__':
    # This won't run when your module is imported by the tests module.
    # Use run_tests to try out some of your own simple tests.
    run_tests()
