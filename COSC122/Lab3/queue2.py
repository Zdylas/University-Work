"""Complete the Queue2 class so that it makes use of the head/tail pointers
Make sure you keep the new doctests given below.
"""
import doctest
import os

os.environ['TERM'] = 'linux'  # Suppress ^[[?1034h


class Node:
    """A node for a linked list."""

    def __init__(self, item):
        self.item = item
        self.next_node = None


class Queue2:
    """ Implements a Queue using a Linked List with head and tail pointers
    You should be able to copy a lot of your code from your Queue class
    but you will be able to make efficiency gains via the use of a tail pointer
    >>> q = Queue2()
    >>> len(q)
    0
    >>> print(q)
    Queue2: head/front -> None
    >>> result = q.dequeue()
    Traceback (most recent call last):
    ...
    IndexError: Can't dequeue from empty queue.
    >>> print(len(q))
    0
    >>> result2 = q.dequeue()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    IndexError: Can't dequeue from empty queue.
    >>> q.enqueue('a')
    >>> print(q)
    Queue2: head/front -> a -> None
    >>> print(q.tail.item)
    a
    >>> print(q.head.item)
    a
    >>> len(q)
    1
    >>> q.dequeue()
    'a'
    >>> len(q)
    0
    >>> q.enqueue('a')
    >>> q.enqueue('b')
    >>> print(q)
    Queue2: head/front -> a -> b -> None
    >>> q.enqueue('c')
    >>> print(q)
    Queue2: head/front -> a -> b -> c -> None
    >>> len(q)
    3
    >>> q.dequeue()
    'a'
    >>> print(q)
    Queue2: head/front -> b -> c -> None
    >>> q.enqueue('z')
    >>> print(q.head.item)
    b
    >>> print(q.tail.item)
    z
    >>> q.dequeue()
    'b'
    >>> q.dequeue()
    'c'
    >>> q.dequeue()
    'z'
    >>> print(q.head)
    None
    >>> print(q.tail)
    None
    """

    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, item):
        """Add an item onto the tail of the queue."""
        # ---start student section---
        temp = Node(item)
        if self.is_empty():
            self.head = temp
        else:
            self.tail.next_node = temp

        self.tail = temp
        # ===end student section===

    def dequeue(self):
        """Remove an item from the head of the queue and return it.
        If queue is empty you should raise an IndexError as per
        the comment below."""
        # use the following line to raise error if stack is empty
        # raise IndexError("Can't dequeue from empty queue.")
        # ---start student section---
        if self.is_empty():
            raise IndexError("Can't dequeue from empty queue.")
        else:
            current = self.head
            self.head = current.next_node
            if self.head == None:
                self.tail = None
            return current.item

        # ===end student section===

    def is_empty(self):
        """ Returns True if the Queue is empty """
        # ---start student section---
        if self.head == None:
            return True
        return False
        # ===end student section===

    def __len__(self):
        """ Returns the length --- calling len(q) will invoke this method"""
        # ---start student section---
        current = self.head
        count = 0
        while current != None:
            count += 1
            current = current.next_node

        return count
        # ===end student section===

    def __str__(self):
        """Returns a string representation of the list for the queue
        starting from the beginning of the list.
        Items are separated by ->
        and ending with -> None
        eg, Queue2: head/front -> a -> b -> None
        See doctests in class docstring
        """
        result = 'Queue2: head/front'
        current = self.head
        while current is not None:
            result += ' -> ' + str(current.item)
            current = current.next_node
        result += ' -> None'
        return result


def main():
    """ Mainly tests """
    # set verbose to False to get less doctest output
    verbose = True

    # Can enter an infinite loop if Queue2 isn't implemented correctly
    result = doctest.testmod()
    if verbose:
        print(result)


if __name__ == '__main__':
    main()
