"""
classes3.py
Assignment 3 COSC122 Assignment

This module provides classes that are to be used to complete assignment 3 .
These have many careful restrictions, but do provide a sufficient interface
to solve the problems given.
"""
from stats import StatCounter, PLATE_COMPS, PRIORITY_COMPS
from abc import ABC, abstractmethod

MIN_PLATE_SIZE = 6
CHARACTER_ERROR = 'Number plates must only contain capital letters or digits: '
ERROR_TEMPLATE = 'NumberPlates must be at least {} characters. '
PLATE_LENGTH_ERROR = ERROR_TEMPLATE.format(MIN_PLATE_SIZE)

PLATE_COMPARISON_TYPE_ERROR = 'NumberPlates can only be compared to other NumberPlates. '
PRIORITY_COMPARISON_TYPE_ERROR = "Priority objects can only be compared to Priority objects"


def _fnv32a_hash(string):
    """ A nice fast little hashing function :)
    You shouldn't use this directly.
    You should use expressions such as hash(my_number_plate)
       see the __hash__ method in the NumberPlate class.
    """
    hval = 0x811c9dc5
    fnv_32_prime = 0x01000193
    uint32_max = 2 ** 32
    for c in string:
        hval = hval ^ ord(c)
        hval = (hval * fnv_32_prime) % uint32_max
    # The result is trimmed down to 31 bits (plus a sign bit) to give
    # consistent results on 32 and 64 bit systems
    # Otherwise hash() will implicitly do this
    # based on build of Python
    # see https://docs.python.org/3/reference/datamodel.html#object.__hash__
    # & is then binary and operation
    hval = hval & 0b1111111111111111111111111111111
    return hval


class NumberPlate(object):
    """ A simple variation on strings so actual comparisons 
    and hashes can be counted.
    """

    def __init__(self, plate):
        """ plate should be a string containing only uppercase letter and digits.
        It should have at least MIN_PLATE_SIZE characters 
        """
        if not all(('A' <= c <= 'Z') or ('0' <= c <= '9') for c in plate):
            raise ValueError(CHARACTER_ERROR + ' ' + plate)
        if len(plate) < MIN_PLATE_SIZE:
            raise ValueError(PLATE_LENGTH_ERROR)
        self._plate = plate

    def __repr__(self):
        return repr(self._plate)

    def __str__(self):
        return str(self._plate)

    def __eq__(self, other):
        if not isinstance(other, NumberPlate):
            print(type(other))
            raise TypeError(PLATE_COMPARISON_TYPE_ERROR)
        StatCounter.increment(PLATE_COMPS)
        return self._plate == other._plate

    def __le__(self, other):
        if not isinstance(other, NumberPlate):
            raise TypeError(PLATE_COMPARISON_TYPE_ERROR)
        StatCounter.increment(PLATE_COMPS)
        return self._plate <= other._plate

    def __ne__(self, other):
        if not isinstance(other, NumberPlate):
            raise TypeError(PLATE_COMPARISON_TYPE_ERROR)
        StatCounter.increment(PLATE_COMPS)
        return self._plate != other._plate

    def __lt__(self, other):
        if not isinstance(other, NumberPlate):
            raise ValueError(PLATE_COMPARISON_TYPE_ERROR)
        StatCounter.increment(PLATE_COMPS)
        return self._plate < other._plate

    def __gt__(self, other):
        if not isinstance(other, NumberPlate):
            raise ValueError(PLATE_COMPARISON_TYPE_ERROR)
        StatCounter.increment(PLATE_COMPS)
        return self._plate > other._plate

    def __ge__(self, other):
        if not isinstance(other, NumberPlate):
            raise ValueError(PLATE_COMPARISON_TYPE_ERROR)
        StatCounter.increment(PLATE_COMPS)
        return self._plate >= other._plate

    def __hash__(self):
        """ hash(my_number_plate) will use this method, ie, it will 
        return the hash value for my_number_plate.
        """
        return _fnv32a_hash(self._plate)

    def __getattr__(self, attr):
        """All other behaviours use self._plate.
        You probably shouldn't be using any other methods though...
        """
        return self._plate.__getattribute__(attr)


class Priority(object):
    """ A simple variation on ints so that we can count comparisons. """

    def __init__(self, priority):
        self._priority = priority

    def __repr__(self):
        return repr(self._priority)

    def __str__(self):
        return str(self._priority)

    def __eq__(self, other):
        if not isinstance(other, Priority):
            raise ValueError(PRIORITY_COMPARISON_TYPE_ERROR)
        StatCounter.increment(PRIORITY_COMPS)
        return self._priority == other._priority

    def __le__(self, other):
        if not isinstance(other, Priority):
            raise ValueError(PRIORITY_COMPARISON_TYPE_ERROR)
        StatCounter.increment(PRIORITY_COMPS)
        return self._priority <= other._priority

    def __ne__(self, other):
        if other is None:
            StatCounter.increment(PRIORITY_COMPS)
            return False
        if not isinstance(other, Priority):
            raise ValueError(PRIORITY_COMPARISON_TYPE_ERROR)
        StatCounter.increment(PRIORITY_COMPS)
        return self._priority != other._priority

    def __lt__(self, other):
        if not isinstance(other, Priority):
            raise ValueError(PRIORITY_COMPARISON_TYPE_ERROR)
        StatCounter.increment(PRIORITY_COMPS)
        return self._priority < other._priority

    def __gt__(self, other):
        if not isinstance(other, Priority):
            raise ValueError(PRIORITY_COMPARISON_TYPE_ERROR)
        StatCounter.increment(PRIORITY_COMPS)
        return self._priority > other._priority

    def __ge__(self, other):
        if not isinstance(other, Priority):
            raise ValueError(PRIORITY_COMPARISON_TYPE_ERROR)
        StatCounter.increment(PRIORITY_COMPS)
        return self._priority >= other._priority

    def __hash__(self):
        """ As priorities are just integers, just return the priority itself """
        return self._priority

    def __getattr__(self, attr):
        """All other behaviours use self._priority.
        You probably shouldn't be using any other methods though...
        """
        return self._priority.__getattribute__(attr)


class Car(object):

    def __init__(self, plate, location, dodgy_factor):
        """ A car object to hold all the information needed to
            store them in a car queue. It has the following atributtes...
            plate: a NumberPlate object or string representing a number plate
                simple strings will be converted to NumberPlates.
            location: is a tuple (x_coordinate, y_coordinate) for the grid location
            dodgy_factor: a value between 0 and 100 for dodgyness
                A higher dodgy factor means the car belongs to a more dodgy person.
                For example, axe psychopathic axe murderers should come in at 100
                and people with overdue parking tickets would be much lower.
            plate: should be a string containing only uppercase letter and digits.
                It should have at least MIN_PLATE_SIZE characters
        """
        if isinstance(plate, str):
            plate = NumberPlate(plate)
        self.plate = plate
        self.location = location
        x_coord, y_coord = self.location
        self.distance_to_station = (
            (x_coord * x_coord) + (y_coord * y_coord)) ** 0.5
        self.dodgy_factor = dodgy_factor
        self.priority = Priority(self._calc_priority())

    def _calc_priority(self):
        """ Low priority values should be visited before high priority values
        because they are closer or more dodgy
        
        Note: This method is PRIVATE (name begins with _) and should only be
        used within this class, do not use it in your code to get the priority.
        """
        return int(self.distance_to_station * (1 - self.dodgy_factor / 100))

    def __repr__(self):
        return "Car({}, {}, {}, {})".format(repr(self.plate),
                                            self.location,
                                            self.dodgy_factor,
                                            self.priority)


