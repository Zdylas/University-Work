

"""
tests.py
A module of unit tests to verify your answers.

These unit tests aren't going to be that useful for debugging!
Don't be too worried if you can't understand how they work.
You should be able to understand the output though...

We recommend starting testing yourself with small heaps so that you can
verify your results by hand.

"""
import os
import shutil
from stats import IS_MARKING_MODE
import signal
import math
import utilities
import time
import string
import unittest
import sys

from classes3 import NumberPlate, Priority, Car
from utilities import read_heap_test_data, run_heap_tests
from stats import StatCounter, PRIORITY_COMPS
from car_queue import *

# to allow you to use recursion for sift up and down with big 1-heaps :)
sys.setrecursionlimit(2100)

TEST_DIR = './test_data/'
TEST_FILE_FORMAT = TEST_DIR + \
    "{imports}-{enqueues}-{dequeues}-{updates}-{removes}-a.txt"

# the default max number of children to test up to
# some classes may go even higher, eg, for bigger data sets
DEFAULT_MAX_NUM_CHILDREN_TO_TEST = 8


get_real_count = StatCounter.get_count
set_real_count = StatCounter.set_count



def log_base_k(k, n):
    """ Returns log base k of n
    That is k to the power of result is n"""
    result = math.log2(n) / math.log2(k)
    return result


class HeapAssertions:

    def assertHeap(self, heap, operation, index=0):
        """ AssertHeap is an O(n) check that the heap is valid.
            Operation is a string indicating the operation after
            which the assertHeap is being run.
        """
        child_indices = heap._indices_of_children(index)
        valid_child_indices = [i for i in child_indices if i < len(heap._data)]
        if not valid_child_indices:
            return  # No children, no worries!
        parent_value = heap._data[index]
        for i in valid_child_indices:
            child_value = heap._data[i]
            if child_value.priority < parent_value.priority:
                raise AssertionError("Bad heap invariant after '{}':"
                                     "\n\tparent: {}\n\tchild: {}".format(
                                         operation, parent_value, child_value
                                     ))
            self.assertHeap(heap, operation, index=i)

    def assertIndices(self, heap):
        """ AssertIndices checks that the index dictionary is correct!
        """
        for plate, index in heap._indices.items():
            if heap._data[index].plate != plate:
                raise AssertionError("Index is not pointing to the right place:"
                                     "\n\tExpected {} at index {}, but found {}."
                                     "".format(plate, index, heap._data[index].plate))


class BaseTestCarQueue(unittest.TestCase, HeapAssertions):

    def setUp(self):
        """Runs before every test case"""
        StatCounter.reset_counts()
        # sub classes can change the following default settings
        self.use_fast_heapify = False  # the default setting

        # set max number of childre that will be tested
        self.max_num_children = DEFAULT_MAX_NUM_CHILDREN_TO_TEST

        # Most tests will change num_children before running
        # set to 2 as a simple default
        self.num_children = 2
        # self.start_time = time.perf_counter()

    def tearDown(self):
        StatCounter.reset_counts()
        # self.end_time = time.perf_counter()
        # test_time = (self.end_time - self.start_time)
        # print(f'{test_time:.4f}s', end=' ')


    def get_import_bounds(self, import_size):
        """ Returns upper and lower bounds for importing the starting list.
            This will be O(n) if using fast heapify
            and O(n log n) if using repetitive enqueuing to the heap
        """
        num_children = self.num_children
        lower_bound = 0
        upper_bound = 0
        if self.use_fast_heapify:
            lower_bound += import_size
            if num_children == 1:
                upper_bound = int((import_size * (import_size - 1)) / 2) + 1
            else:
                upper_bound += 2 * import_size + 1
        else:
            # set O(n log n) importing bounds
            lower_bound += import_size - 1
            if num_children == 1:
                upper_bound = int((import_size * (import_size - 1)) / 2 + 1)
            else:
                for i in range(1, import_size + 1):
                    upper_bound += int(log_base_k(num_children,
                                                  i + num_children))
        return lower_bound, upper_bound

    def get_bounds(self, import_size, instructions):
        num_children = self.num_children
        lower_bound, upper_bound = self.get_import_bounds(import_size)
        queue_size = import_size
        op_deltas = {'enqueue': 1, 'dequeue': -1, 'remove': -1, 'update': 0}
        op_factors = {'enqueue': 1,
                      'dequeue': num_children,
                      'remove': num_children,
                      'update': num_children}
        for operation, _ in instructions:
            # Update the bounds for an O(log n) operation (or O(n) for 1-heap)
            if num_children == 1:
                # set to half the expected average less 1
                lower_bound += int((queue_size + 1) / 4 -
                                   1) if queue_size > 0 else 0
                # set to max comps plus 1
                upper_bound += int(queue_size)
            else:
                lower_bound += int(log_base_k(num_children, queue_size) /
                                   4) if queue_size > 0 else 0
                upper_bound += int(op_factors[operation]
                                   * (log_base_k(num_children, queue_size + num_children))) + 1
            queue_size += op_deltas[operation]
        return lower_bound, upper_bound  # upper_bound

    def run_test_file_instructions(self, import_data, instructions):
        """ Using the test data in the file described by 'filename',
             run tests on the self.queue_class_to_test  class given.
        """
        #import_data, instructions = read_heap_test_data(filename)
        # setup up queue of the type queue_class_to_test
        queue = self.queue_class_to_test(self.num_children,
                                         import_data)
        saved_comps = get_real_count(PRIORITY_COMPS)
        self.assertHeap(
            queue, ("fast-" if self.use_fast_heapify else "") + "heapify")
        set_real_count(PRIORITY_COMPS, saved_comps)
        for mode, data in instructions:
            if mode == 'enqueue':
                # data is the Car to enqueue
                queue.enqueue(data)
                saved_comps = get_real_count(PRIORITY_COMPS)
                self.assertIn(data, queue._data)
                set_real_count(PRIORITY_COMPS, saved_comps)
            elif mode == 'dequeue':
                # data is plate of the expected car
                expected_plate = data
                result = queue.dequeue()
                self.assertEqual(result.plate, expected_plate)
            elif mode == 'update':
                # data is plate of the car to remove
                updated_car = data
                queue.update(updated_car)
            elif mode == 'remove':
                # data is plate of the car to remove
                plate_to_remove = data
                queue.remove(plate_to_remove)
                saved_comps = get_real_count(PRIORITY_COMPS)
                # check that it was removed
                self.assertNotIn(plate_to_remove, [
                                 car.plate for car in queue._data])
                set_real_count(PRIORITY_COMPS, saved_comps)

            # check that heap is still heapy
            saved_comps = get_real_count(PRIORITY_COMPS)
            self.assertHeap(queue, mode)
            # check that indices are still consistent
            if self.queue_class_to_test == EditableCarHeapQueue:
                self.assertIndices(queue)
            set_real_count(PRIORITY_COMPS, saved_comps)
        return queue

    def heap_test(self, test_file_name):
        """ Test that the heap correctly processes
            the instructions given in the test file.
        """
        import_data, instructions = read_heap_test_data(test_file_name)
        self.run_test_file_instructions(import_data, instructions)
        return True

    def comparisons_test(self, test_file_name):
        """ Test that the number of comparisons that the student made is
            within the expected bounds (provided by self.get_bounds)
        """
        import_data, instructions = read_heap_test_data(test_file_name)
        lower_bound, upper_bound = self.get_bounds(
            len(import_data), instructions)
        queue = self.run_test_file_instructions(import_data, instructions)
        self.assertGreaterEqual(queue.num_comps, lower_bound)
        self.assertLessEqual(queue.num_comps, upper_bound)
        return True

    def internal_comparisons_test(self, test_file_name):
        """ Test that the student has correctly counted the code against what
            we have counted. This does not mean that the count is correct, just
            that it was correctly counted.
        """
        import_data, instructions = read_heap_test_data(test_file_name)
        queue = self.run_test_file_instructions(import_data, instructions)
        self.assertEqual(queue.num_comps,
                         get_real_count(PRIORITY_COMPS))
        return True

    def run_test_series(self, test_file_name, test_method):
        for num_children in range(1, self.max_num_children):
            self.setUp()  # need this between tests as subTest doesn't call setup
            passed = False
            with self.subTest(num_children=num_children):
                self.num_children = num_children
                test_method(test_file_name)
            if not passed:
                break


class TestCarQueueEnqueueTiny(BaseTestCarQueue):
    """ Unit tests for enqueueing (which tests sift_up)
    """

    def test_0010_tiny_enqueue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=0, updates=0, removes=0)
        self.run_test_series(test_file, self.heap_test)

    def test_0020_tiny_enqueue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=0, updates=0, removes=0)
        self.run_test_series(test_file, self.internal_comparisons_test)

    def test_0030_tiny_enqueue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=0, updates=0, removes=0)
        self.run_test_series(test_file, self.comparisons_test)


class TestCarQueueEnqueueSmall(BaseTestCarQueue):
    """ Unit tests for enqueueing (which tests sift_up)
    """

    def test_0040_small_enqueue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=10, dequeues=0, updates=0, removes=0)
        self.run_test_series(test_file, self.heap_test)

    def test_0050_small_enqueue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=10, dequeues=0, updates=0, removes=0)
        self.run_test_series(test_file, self.internal_comparisons_test)

    def test_0060_small_enqueue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=10, dequeues=0, updates=0, removes=0)
        self.run_test_series(test_file, self.comparisons_test)


class TestCarQueueEnqueueMedium(BaseTestCarQueue):
    """ Unit tests for enqueueing (which tests sift_up)
    """

    def test_0070_medium_enqueue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=0, updates=0, removes=0)
        self.run_test_series(test_file, self.heap_test)

    def test_0080_medium_enqueue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=0, updates=0, removes=0)
        self.run_test_series(test_file, self.internal_comparisons_test)

    def test_0090_medium_enqueue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=0, updates=0, removes=0)
        self.run_test_series(test_file, self.comparisons_test)


class TestCarQueueEnqueueLarge(BaseTestCarQueue):
    """ Unit tests for enqueueing (which tests sift_up)
    """

    def test_0100_large_enqueue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=0, updates=0, removes=0)
        self.run_test_series(test_file, self.heap_test)

    def test_0110_large_enqueue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=0, updates=0, removes=0)
        self.run_test_series(test_file, self.internal_comparisons_test)

    def test_0120_large_enqueue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=0, updates=0, removes=0)
        self.run_test_series(test_file, self.comparisons_test)


class TestCarQueueEnqueueHuge(BaseTestCarQueue):
    """ Unit tests for enqueueing (which tests sift_up)
    """

    def test_0130_huge_enqueue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=1000, dequeues=0, updates=0, removes=0)
        self.run_test_series(test_file, self.heap_test)

    def test_0140_huge_enqueue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=1000, dequeues=0, updates=0, removes=0)
        self.run_test_series(test_file, self.internal_comparisons_test)

    def test_0150_huge_enqueue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=1000, dequeues=0, updates=0, removes=0)
        self.run_test_series(test_file, self.comparisons_test)


class TestCarQueueDequeueTiny(BaseTestCarQueue):
    """ Unit tests for enqueueing (which tests sift_up) """

    def test_0210_tiny_dequeue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=1, updates=0, removes=0)
        self.run_test_series(test_file, self.heap_test)

    def test_0220_tiny_dequeue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=1, updates=0, removes=0)
        self.run_test_series(test_file, self.internal_comparisons_test)

    def test_0230_tiny_dequeue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=1, updates=0, removes=0)
        self.run_test_series(test_file, self.comparisons_test)


class TestCarQueueDequeueSmall(BaseTestCarQueue):

    def test_0240_small_dequeue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=10, enqueues=10, dequeues=20, updates=0, removes=0)
        self.run_test_series(test_file, self.heap_test)

    def test_0250_small_dequeue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=10, enqueues=10, dequeues=20, updates=0, removes=0)
        self.run_test_series(test_file, self.internal_comparisons_test)

    def test_0260_small_dequeue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=10, enqueues=10, dequeues=20, updates=0, removes=0)
        self.run_test_series(test_file, self.comparisons_test)


class TestCarQueueDequeueMedium(BaseTestCarQueue):

    def test_0270_medium_dequeue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=75, updates=0, removes=0)
        self.run_test_series(test_file, self.heap_test)

    def test_0280_medium_dequeue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=75, updates=0, removes=0)
        self.run_test_series(test_file, self.heap_test)

    def test_0290_medium_dequeue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=75, updates=0, removes=0)
        self.run_test_series(test_file, self.comparisons_test)


class TestCarQueueDequeueLarge(BaseTestCarQueue):

    def test_0300_large_dequeue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=150, updates=0, removes=0)
        self.run_test_series(test_file, self.heap_test)

    def test_0310_large_dequeue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=150, updates=0, removes=0)
        self.run_test_series(test_file, self.internal_comparisons_test)

    def test_0320_large_dequeue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=150, updates=0, removes=0)
        self.run_test_series(test_file, self.comparisons_test)


class TestCarQueueDequeueHuge(BaseTestCarQueue):

    def test_0330_huge_dequeue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=1000, dequeues=1500, updates=0, removes=0)
        self.run_test_series(test_file, self.heap_test)

    def test_0340_huge_dequeue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=1000, dequeues=1500, updates=0, removes=0)
        self.run_test_series(test_file, self.internal_comparisons_test)

    def test_0350_huge_dequeue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=1000, dequeues=1500, updates=0, removes=0)
        self.run_test_series(test_file, self.comparisons_test)


# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# ---------------------------- Now it's time to test Update -------------------------
# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

class TestCarQueueUpdateTiny(BaseTestCarQueue):
    """ Unit tests for updating cars.
        This dataset actually tests everything, because why not.
    """

    def test_0410_tiny_update(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=0, updates=1, removes=0)
        self.run_test_series(test_file, self.heap_test)

    def test_0420_tiny_update_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=0, updates=1, removes=0)
        self.run_test_series(test_file, self.internal_comparisons_test)

    def test_0430_tiny_update_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=0, updates=1, removes=0)
        self.run_test_series(test_file, self.comparisons_test)


class TestCarQueueUpdateSmall(BaseTestCarQueue):

    def test_0440_small_update(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=10, dequeues=5, updates=5, removes=0)
        self.run_test_series(test_file, self.heap_test)

    def test_0450_small_update_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=10, dequeues=5, updates=5, removes=0)
        self.run_test_series(test_file, self.internal_comparisons_test)

    def test_0460_small_update_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=10, dequeues=5, updates=5, removes=0)
        self.run_test_series(test_file, self.comparisons_test)


class TestCarQueueUpdateMedium(BaseTestCarQueue):

    def test_0470_medium_update(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=50, updates=25, removes=0)
        self.run_test_series(test_file, self.heap_test)

    def test_0480_medium_update_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=50, updates=25, removes=0)
        self.run_test_series(test_file, self.internal_comparisons_test)

    def test_0490_medium_update_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=50, updates=25, removes=0)
        self.run_test_series(test_file, self.comparisons_test)


class TestCarQueueUpdateLarge(BaseTestCarQueue):

    def test_0500_large_update(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=150, updates=50, removes=0)
        self.run_test_series(test_file, self.heap_test)

    def test_0510_large_update_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=150, updates=50, removes=0)
        self.run_test_series(test_file, self.internal_comparisons_test)

    def test_0520_large_update_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=150, updates=50, removes=0)
        self.run_test_series(test_file, self.comparisons_test)


class TestCarQueueUpdateHuge(BaseTestCarQueue):

    def test_0530_huge_update(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=100, dequeues=1000, updates=100, removes=0)
        self.run_test_series(test_file, self.heap_test)

    def test_0540_huge_update_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=100, dequeues=1000, updates=100, removes=0)
        self.run_test_series(test_file, self.internal_comparisons_test)

    def test_0550_huge_update_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=100, dequeues=1000, updates=100, removes=0)
        self.run_test_series(test_file, self.comparisons_test)


class TestCarQueueRemoveTiny(BaseTestCarQueue):
    """ Unit tests for removing patients.
        This dataset actually tests everything, because why not."""

    def test_tiny_remove(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=0, updates=0, removes=1)
        self.run_test_series(test_file, self.heap_test)

    def test_tiny_remove_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=0, updates=0, removes=1)
        self.run_test_series(test_file, self.internal_comparisons_test)

    def test_tiny_remove_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=0, updates=0, removes=1)
        self.run_test_series(test_file, self.comparisons_test)


class TestCarQueueRemoveSmall(BaseTestCarQueue):

    def test_small_remove(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=10, dequeues=5, updates=0, removes=5)
        self.run_test_series(test_file, self.heap_test)

    def test_small_remove_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=10, dequeues=5, updates=0, removes=5)
        self.run_test_series(test_file, self.internal_comparisons_test)

    def test_small_remove_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=10, dequeues=5, updates=0, removes=5)
        self.run_test_series(test_file, self.comparisons_test)


class TestCarQueueRemoveMedium(BaseTestCarQueue):

    def test_medium_remove(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=50, updates=0, removes=25)
        self.run_test_series(test_file, self.heap_test)

    def test_medium_remove_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=50, updates=0, removes=25)
        self.run_test_series(test_file, self.internal_comparisons_test)

    def test_medium_remove_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=50, updates=0, removes=25)
        self.run_test_series(test_file, self.comparisons_test)


class TestCarQueueRemoveLarge(BaseTestCarQueue):

    def test_large_remove(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=150, updates=0, removes=50)
        self.run_test_series(test_file, self.heap_test)

    def test_large_remove_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=150, updates=0, removes=50)
        self.run_test_series(test_file, self.internal_comparisons_test)

    def test_large_remove_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=150, updates=0, removes=50)
        self.run_test_series(test_file, self.comparisons_test)


class TestCarQueueRemoveHuge(BaseTestCarQueue):

    def test_huge_remove(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=100, dequeues=1000, updates=0, removes=100)
        self.run_test_series(test_file, self.heap_test)

    def test_huge_remove_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=100, dequeues=1000, updates=0, removes=100)
        self.run_test_series(test_file, self.internal_comparisons_test)

    def test_huge_remove_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=100, dequeues=1000, updates=0, removes=100)
        self.run_test_series(test_file, self.comparisons_test)


class TestTaskTwoBase(BaseTestCarQueue):
    # Test enqueue in CarHeapQueue
    # Uses normal heapify

    def setUp(self):
        super().setUp()
        self.queue_class_to_test = CarHeapQueue
        self.use_fast_heapify = False


class TestTaskTwoTiny(TestTaskTwoBase, TestCarQueueEnqueueTiny):
    pass


class TestTaskTwoSmall(TestTaskTwoBase, TestCarQueueEnqueueSmall):
    pass


class TestTaskTwoMedium(TestTaskTwoBase, TestCarQueueEnqueueMedium):
    pass


class TestTaskTwoLarge(TestTaskTwoBase, TestCarQueueEnqueueLarge):
    pass


class TestTaskTwoHuge(TestTaskTwoBase, TestCarQueueEnqueueHuge):
    pass


class TestTaskTwoAll(TestTaskTwoBase, TestCarQueueEnqueueTiny,
                     TestCarQueueEnqueueSmall, TestCarQueueEnqueueMedium,
                     TestCarQueueEnqueueLarge, TestCarQueueEnqueueHuge):
    pass


class TestTaskThreeBase(BaseTestCarQueue):
    # Test dequeue in CarHeapQueue
    # Uses normal heapify

    def setUp(self):
        super().setUp()
        self.queue_class_to_test = CarHeapQueue
        self.use_fast_heapify = False



class TestTaskThreeTiny(TestTaskThreeBase, TestCarQueueDequeueTiny):
    pass


class TestTaskThreeSmall(TestTaskThreeBase, TestCarQueueDequeueSmall):
    pass


class TestTaskThreeMedium(TestTaskThreeBase, TestCarQueueDequeueMedium):
    pass


class TestTaskThreeLarge(TestTaskThreeBase, TestCarQueueDequeueLarge):
    pass


class TestTaskThreeHuge(TestTaskThreeBase, TestCarQueueDequeueHuge):
    pass


class TestTaskThreeAll(TestTaskThreeBase, TestCarQueueDequeueTiny,
                       TestCarQueueDequeueSmall, TestCarQueueDequeueMedium,
                       TestCarQueueDequeueLarge, TestCarQueueDequeueHuge):
    pass




class TestTaskFourBase(BaseTestCarQueue):
    # Test update, using an editable queue

    def setUp(self):
        super().setUp()
        self.queue_class_to_test = EditableCarHeapQueue
        self.use_fast_heapify = False



class TestTaskFourTiny(TestTaskFourBase, TestCarQueueUpdateTiny):
    pass


class TestTaskFourSmall(TestTaskFourBase, TestCarQueueUpdateSmall):
    pass


class TestTaskFourMedium(TestTaskFourBase, TestCarQueueUpdateMedium):
    pass


class TestTaskFourLarge(TestTaskFourBase, TestCarQueueUpdateLarge):
    pass


class TestTaskFourHuge(TestTaskFourBase, TestCarQueueUpdateHuge):
    pass


class TestTaskFourAll(TestTaskFourBase, TestCarQueueUpdateTiny,
                      TestCarQueueUpdateSmall, TestCarQueueUpdateMedium,
                      TestCarQueueUpdateLarge, TestCarQueueUpdateHuge):
    pass


class TestTaskFiveBase(BaseTestCarQueue):
    # Test removing from an editable queue

    def setUp(self):
        super().setUp()
        self.queue_class_to_test = EditableCarHeapQueue
        self.use_fast_heapify = False


class TestTaskFiveTiny(TestTaskFiveBase, TestCarQueueRemoveTiny):
    pass


class TestTaskFiveSmall(TestTaskFiveBase, TestCarQueueRemoveSmall):
    pass


class TestTaskFiveMedium(TestTaskFiveBase, TestCarQueueRemoveMedium):
    pass


class TestTaskFiveLarge(TestTaskFiveBase, TestCarQueueRemoveLarge):
    pass


class TestTaskFiveHuge(TestTaskFiveBase, TestCarQueueRemoveHuge):
    pass


class TestTaskFiveAll(TestTaskFiveBase, TestCarQueueRemoveTiny,
                      TestCarQueueRemoveSmall, TestCarQueueRemoveMedium,
                      TestCarQueueRemoveLarge, TestCarQueueRemoveHuge):
    pass


def all_tests_suite():
    """ 
    Makes a suite that includes the tests you want to run.
    """
    suite = unittest.TestSuite()

    # Task 2 - Enqueue
    #suite.addTest(unittest.makeSuite(TestTaskTwoTiny))
    #suite.addTest(unittest.makeSuite(TestTaskTwoSmall))
    #suite.addTest(unittest.makeSuite(TestTaskTwoMedium))
    #suite.addTest(unittest.makeSuite(TestTaskTwoLarge))
    #suite.addTest(unittest.makeSuite(TestTaskTwoHuge))
    suite.addTest(unittest.makeSuite(TestTaskTwoAll))

    # uncomment the following lines when ready to test further tasks...

    # Task 3 - Dequeue
    #suite.addTest(unittest.makeSuite(TestTaskThreeTiny))
    #suite.addTest(unittest.makeSuite(TestTaskThreeSmall))
    #suite.addTest(unittest.makeSuite(TestTaskThreeMedium))
    #suite.addTest(unittest.makeSuite(TestTaskThreeLarge))
    #suite.addTest(unittest.makeSuite(TestTaskThreeHuge))
    # suite.addTest(unittest.makeSuite(TestTaskThreeAll))

    # OPTIONAL Task 1 - update with the EditableCarHeapqueue
    # suite.addTest(unittest.makeSuite(TestTaskFourAll))

    # OPTIONAL Task 2 - remove with the EditableCarHeapqueue
    # suite.addTest(unittest.makeSuite(TestTaskFiveAll))

    return suite




def main():
    """ Makes a test suite and runs it. Will your code pass? """
    test_runner = unittest.TextTestRunner(verbosity=2)
    all_tests = all_tests_suite()
    test_runner.run(all_tests)


if __name__ == '__main__':
    main()
