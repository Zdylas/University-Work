import time
import random
from quicksort import *
from matplotlib import pyplot
import sys

# Get the time units given by the perf_counter
# Note: time.clock has been deprecated in Python 3.3
# and replaced with the more precise perf_counter method

# define time.get_time to be the appropriate time counter
if sys.version_info < (3, 3):
    get_time = time.clock
    print("Using time.clock for timing - Python ver < 3.3")
else:
    get_time = time.perf_counter
    print("Using time.perf_counter for timing - Python ver >= 3.3")
    REZ = time.get_clock_info('perf_counter').resolution
    print('One unit of time is ' + str(REZ) + ' seconds')


n_trials = 100

# n is used to denote how many numbers are to be sorted

# list_of_ns is a list of the size of lists to time sorting
# initially [40, 80, 120 ... 760]
# list_of_ns will be used as the x-axis on your graphs
# and average time will be plotted on the y-axis
list_of_ns = list(range(40, 800, 40))


# consider converting this code into a function that takes
# list_of_ns, pivot_type, and randomise_numbers as parameters
# and returns a list of average times for each of the ns
avg_times = []
# we will run the testing for each give data size
for n in list_of_ns:
    total_time = 0
    # run the sort many times and take the average time
    # to get the average sum the time across all trials
    # then divide by the number of trials
    for i in range(n_trials):
        numbers_to_sort = list(range(n))  # a sorted list
        # randomise the numbers_to_sort here if you want to test random data
        start = get_time()
        s = quicksort(numbers_to_sort, 'left-pivot')
        end = get_time()
        time_taken = end - start
        total_time += time_taken
    avg_time = total_time / n_trials
    # print(n, avg_time)  # see what's happening
    avg_times.append(avg_time)


# You don't need to graph anything to answer the lab quiz questions
# But it's always fun to visualise what is going on
# If you want to get the average time for just one data size
# you could make the list_of_ns a list with just one number
# for example list_of_ns = [760] :)

# some quick and dirty plotting
pyplot.plot(list_of_ns, avg_times, 'bo')
pyplot.title(f"Time vs. List size, average of {n_trials} trials")
pyplot.xlabel('n')
pyplot.ylabel('Average Time per sort')
pyplot.show()


# to add more lines to the plot simply add more triples to the pyplot.plot call
# eg, pyplot.plot(list_of_ns, avg_times_sorted, 'bo',
#                 list_of_ns, avg_times_random, 'go')
