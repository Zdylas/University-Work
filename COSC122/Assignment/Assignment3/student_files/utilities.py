""" Various utilities for assignment part 3 """

from classes3 import NumberPlate, Priority, Car
from car_queue import *


def verify_heapness(heap, index=0):
    """ Make sure that the heap invariant is maintained. """
    child_indices = heap._indices_of_children(index)
    valid_child_indices = [i for i in child_indices if i < len(heap)]
    if not valid_child_indices:
        return True  # No children, no worries!
    parent_value = heap._data[index]
    for i in valid_child_indices:
        child_value = heap._data[i]
        if child_value.priority < parent_value.priority:
            return False
        if not verify_heapness(heap, index=i):
            return False
    return True


def verify_indices(editable_heap):
    """ Returns True if the index dictionary is correct! """
    for plate, index in editable_heap._indices.items():
        if editable_heap._data[index].plate != plate:
            return False
    return True


def run_heap_tests(filename, priority_queue, num_children, verbose=True):
    """ Using the test data in the file described by 'filename', run tests on the
        'priority_queue' class given. E.g.,
            run_tests('./test_data/0-1-0-0-0-a.txt', CarHeapQueue)
    """
    import_data, instructions = read_heap_test_data(filename)
    queue = priority_queue(num_children, import_data)
    if verbose:
        print('Initial after import:')
        print(queue)
    always_heap_like = True
    for mode, data in instructions:
        if mode == 'enqueue':
            car_to_enqueue = data
            if verbose:
                print("Enqueueing {}".format(data))
            queue.enqueue(car_to_enqueue)
        elif mode == 'dequeue':
            expected_plate = data
            dequeued_plate = queue.dequeue().plate
            if verbose:
                print("Dequeued {}, which is {}".format(
                    dequeued_plate, "right" if dequeued_plate == expected_plate else "wrong"))
        elif mode == 'remove':
            plate_to_remove = data
            if verbose:
                print("Removing {}".format(plate_to_remove))
            queue.remove(plate_to_remove)
        elif mode == 'update':
            car_to_update = data
            if verbose:
                print("Updating {}".format(car_to_update))
            queue.update(car_to_update)

        if not verify_heapness(queue):
            raise AssertionError("Whoops, heap invariant violated!")
        if isinstance(priority_queue, EditableCarHeapQueue):
            if not verify_indices(priority_queue):
                raise AssertionError(
                    "Whoops, indices don't match acutal indices of cars!")
    return queue


def create_car_from_line(information):
    """ Create a car from a line of information.
    """
    plate_str, x_coord_raw, y_coord_raw, dodgy_factor_raw = information.strip().split(",")
    plate = NumberPlate(plate_str)
    x_coord = int(x_coord_raw)
    y_coord = int(y_coord_raw)
    dodgy_factor = int(dodgy_factor_raw)
    return Car(plate, (x_coord, y_coord), dodgy_factor)


def read_heap_test_data(filename):
    """ Read in the test data from the file given by filename.
    Returns the list of Cars to import/start the queue with and
    a list of command, data tuples.
    The comman, data tuples will be in one of the following forms:
    ('enqueue', car_object)
    ('dequeue', NumberPlate_of_expected_car_object)
    ('remove', NumberPlate_of_car_to_remove)
    This data will be used by run_heap_tests - in this module
    and run_test_file_instructions - in the test_car_queue module.
    """
    import_data = []
    instructions = []
    with open(filename) as infile:
        n_imports = int(infile.readline())
        for _ in range(n_imports):
            line = infile.readline().strip()
            import_data.append(create_car_from_line(line))
        infile.readline()  # skip blank line
        enqueues, dequeues, updates, removes = [
            int(i) for i in infile.readline().split(',')]
        n_enqueues_loaded = 0
        n_dequeues_loaded = 0
        n_updates_loaded = 0
        n_removes_loaded = 0
        for line in infile.readlines():
            instruction, information = line.split(maxsplit=1)
            if instruction == 'enqueue':  # Enqueue the car
                instructions.append(
                    ('enqueue', create_car_from_line(information)))
                n_enqueues_loaded += 1
            elif instruction == 'dequeue':  # Dequeue a car, should assert match with given name
                plate_of_dequeued_car = NumberPlate(information.strip())
                instructions.append(('dequeue', plate_of_dequeued_car))
                n_dequeues_loaded += 1
            elif instruction == 'update':  # update with new car
                # information is a car
                updated_car = create_car_from_line(information)
                instructions.append(('update', updated_car))
                n_updates_loaded += 1
            elif instruction == 'remove':  # Remove the named car
                # information is just a name, not a car
                plate_of_removed_car = NumberPlate(information.strip())
                instructions.append(('remove', plate_of_removed_car))
                n_removes_loaded += 1
            else:
                raise NameError("Priority Queue instruction not understood.")
        # check that we got as many as expected
        assert n_enqueues_loaded == enqueues
        assert n_dequeues_loaded == dequeues
        assert n_updates_loaded == updates
        assert n_removes_loaded == removes
    return import_data, instructions


def read_plate_block(lines, index):
    """ Makes a list of all the plates starting from
    the line with the given index, up until a blank line
    is reached - the blank line indicates the end of the
    section of plate date.
    Returns the list of number plates along with the index
    of the blank line
    """
    plate_list = []
    num_lines = len(lines)
    done = False
    while index < num_lines and not done:
        current_line = lines[index]
        if current_line != '\n':
            for item in current_line.strip().split(' '):
                plate_list.append(NumberPlate(item))
            index += 1
        else:
            done = True
    return plate_list, index


def read_unique_test_data(filename):
    """ Returns list1, list2 and expected lists from a unique test file.
    The files are named unique-n1-n2-nexp-seed
    where
    n1 = length of list1
    n2 = length of list2
    nexp = expected number of unique items in list2
    seed = random seed used to generate the file
    """
    with open(filename, encoding='utf-8') as infile:
        lines = infile.readlines()
    i = 0
    _, raw_n1 = lines[i].split('=')
    n1 = int(raw_n1)
    list1, end_index = read_plate_block(lines, i + 1)
    assert len(list1) == n1

    i = end_index + 1  # skip the blank line
    _, raw_n2 = lines[i].split('=')
    n2 = int(raw_n2)
    list2, end_index = read_plate_block(lines, i + 1)
    assert len(list2) == n2

    i = end_index + 1  # skip the blank line
    _, n_unique_raw = lines[i].split('=')
    n_unique = int(n_unique_raw)
    unique_list, _ = read_plate_block(lines, i + 1)
    assert len(unique_list) == n_unique
    return list1, list2, unique_list


def plates_from_strings(strings):
    """ Returns a list of NumberPlates based on the strings provided.
    The strings must be valid number plates character sequences
    For example 'ABC123' or 'BOB323'
    """
    return [NumberPlate(string) for string in strings]


def simple_unique_file_load_tests():
    """ You can do some uniquely interesting file testing here """
    print('Uniquely interesting')
    list1, list2, uniques = read_unique_test_data(
        './test_data/unique-10-10-4-a.txt')
    print('list1:\n', list1)
    print('list2:\n', list2)
    print('uniques:\n', uniques)
    print('\n' * 10)


def test_making_simple_heaps():
    """ Some examples of loading heaps """
    filename = './test_data/10-10-20-0-0-a.txt'
    print('Making CarHeapQueue from', filename)
    import_data, test_data = read_heap_test_data(filename)
    heap = CarHeapQueue(2, import_data)
    print(heap)
    print('Heap is heapy =', verify_heapness(heap))
    print()
    print('Making EditableCarHeapQueue from', filename)
    heap = EditableCarHeapQueue(2, import_data)
    print(heap)
    print('Heap is heapy =', verify_heapness(heap))
    print('\n' * 5)


def run_some_test_files():
    """ Runs the commands in some test files """
    filename = './test_data/10-10-20-0-0-a.txt'
    print('Running tests on', filename)
    run_heap_tests(filename, CarHeapQueue, 2, fast=False, verbose=True)
    print('\n' * 5)
    filename = './test_data/50-25-50-25-0-a.txt'
    print('Running tests on', filename)
    run_heap_tests(filename, EditableCarHeapQueue, 2, fast=False, verbose=True)


def main():
    """ Keeping it organised since 2018 """
    simple_unique_file_load_tests()
    # test_making_simple_heaps()
    # run_some_test_files()


if __name__ == '__main__':
    main()
