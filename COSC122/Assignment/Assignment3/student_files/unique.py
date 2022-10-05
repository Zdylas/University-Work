""" A unique module of fun.

Author: Your name here
Email: Your email here

"""
from utilities import read_unique_test_data, plates_from_strings
# from classes3 import NumberPlate   # include if you want to make some plates
# from stats import StatCounter, PLATE_COMPS   # if you want to use the StatCounter


def uniques_by_merge_opp(plates1, plates2):
    """ Takes two sorted lists of NumberPlates and
    returns a list that contains NumberPlates that only appear in plates2,
    in the same order as they appear in plates2,
    and an integer that represents the number  of NumberPlate comparisons
    that were made.
    This function should work in a way that is similar to the merge operation
    part of a merge-sort.
    That is, the function should return the tuple (result_list, comparisons).
    There are a few variations that can be used here and our simple test cases
    will expect one of them. You will need to figure out which one. Working
    through the simple examples by hand is recommended.
    """
    result_list = []
    comparisons = 0
    # ---start student section---
    pass
    # ===end student section===
    return result_list, comparisons




# -------------------------------------------------------------------------
# The area below is for your own testing
# Don't submit code below here to the quiz server
# -------------------------------------------------------------------------
def run_file_example():
    """ An example using files """
    print('File example:')
    list1, list2, uniques = read_unique_test_data(
        './test_data/unique-10-10-4-a.txt')
    print('list1:', list1)
    print('list2:', list2)
    print('Expected uniques:', uniques)

    uniques, comparisons = uniques_by_merge_opp(list1, list2)
    print('\nUniques:         ', uniques)
    print('Used {} comparisons'.format(comparisons))
    print('\n' * 4)


def run_from_strings_example():
    """ Example usage plates_from_string function """
    list1 = plates_from_strings(['CUJ035', 'DRA227', 'EEQ923',
                                 'EFD633', 'GPS402', 'HWE173',
                                 'KCX418', 'MQC884', 'NBN256',
                                 'ZDI284'])

    list2 = plates_from_strings(['EFD635', 'GPS402', 'HWE175',
                                 'KCX418', 'MSZ294', 'NBN256',
                                 'NUD891', 'YES436', 'ZDI284',
                                 'ZXZ369'])

    uniques, comparisons = uniques_by_merge_opp(list1, list2)
    print('String example:')
    print('list1:', list1)
    print('list2:', list2)
    print('Uniques:', uniques)
    print('Used {} comparisons'.format(comparisons))
    print('\n' * 4)


def run_my_tests():
    """Run your tests here to keep them tidy"""
    # Put your testing code here so that we don't run it when marking:)

    # example usage plates_from_string function
    run_from_strings_example()

    # a simple file example
    run_file_example()


if __name__ == '__main__':
    run_my_tests()
