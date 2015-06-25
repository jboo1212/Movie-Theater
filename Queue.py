__author__ = 'Sorostitude'

from linkedlist33 import *


class _Queue:

    # Every queue object will start off with
    # an empty LL (linked list).
    def __init__(self):
        self.linked_list = LinkedList()

    # acts like append
    def enqueue(self, item):
        self.linked_list.append(item)

    # acts like remove_first bu4t returns that item as well
    def dequeue(self):
        if self.linked_list.length == 0:
            raise TypeError('Empty Queue')
        else:
            return self.linked_list.remove_first()

    # returns the element after head
    def front(self):
        if self.linked_list.length == 0:
            raise TypeError('Empty Queue')
        else:
            return self.linked_list.head.next

    def __repr__(self):
        return 'Queue({})'.format(self.linked_list)


class Ticket_Line(_Queue):

    def __init__(self):
        # Line number is default 0.
        _Queue.__init__(self)
        self.line_number = 0

    # Increments the line number.
    def increment_line_number(self):
        self.line_number += 1
        return self.line_number

    def __repr__(self):
        return 'Ticket Line'

    def __len__(self):
        return self.linked_list.length


# Make a bare-bones customer class.
class Customer:

    def __init__(self):
        pass
