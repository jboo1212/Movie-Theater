__author__ = 'Sorostitude'

# Node is a custom data structure that stores
# nodes (i.e. data and next pointers).  Python supports
# an implicit reference of a next() call, i.e. you do not
# have to indicate whether or not this is a pointer or a value.


class Node:

    def __init__(self, data, next):
        self.data = data
        self.next = next

    def __str__(self):
        return str(self.data)



class LinkedList():

    length = 0
    head = tail = None

    # Initialize a linked list with no parameters;
    # set head, tail initially to None type.
    def __init__(self):
        self.length = 0
        self.head = Node(None, None)
        self.tail = self.head

    # print_list prints the nodes in Linked List
    def print_list(self):
        node = self.head
        while node:
            # node equals head
            if node == self.head:
                node = node.next
            # node equals tail
            elif node.next is None:
                print node
                return
            # node points to another node
            else:
                print node
                node = node.next

    # append adds a node to the end of the 'list' of nodes
    # 1) the first case is head = tail
    # 2) the second case is head != tail, i.e. head points to a node
    # not equal to tail
    def append(self, data):
        if self.head.next is None:
            node = Node(data, None)
            self.head.next = node
            self.tail = node
            self.length += 1
        else:
            node = Node(data, None)
            self.tail.next = node
            self.tail = node
            self.tail.next = None
            self.length += 1
        return node

    # prepend adds a node to the front of the 'list' of nodes
    # and it takes care of a couple of cases
    def prepend(self, data):
        if self.head.next is None:
            node = Node(data, next=None)
            self.head.next = node
            self.tail = node
            self.length += 1
        # So let's look at this case:
        elif self.head.next == self.tail:
            node = Node(data, next)
            self.head.next = node
            node.next = self.tail
            self.tail.next = None
            self.length += 1
        else:
            node = Node(data, next)
            node.next = self.head.next
            self.head.next = node
            self.length += 1
        return node

    # remove_first removes the first element of the list (self.head.next)
    # How do we remove an element from this class given that it doesn't support
    # del, remove; so I think we need to define a new remove method?
    # So it's obvious that I need to support list functionality
    def remove_first(self):
        if self.length == 0:
            raise TypeError('Tried to remove empty list')
        elif self.head == self.tail:
            ll = [self.head]
            ll.remove(self.head)
            self.length -= 1
        elif self.head.next == self.tail:
            ll = [self.head, self.tail]
            ll.remove(self.tail)
            self.head.next = None
            self.length -= 1
        else:
            node = self.head.next
            ll = [self.head, node]
            self.head.next = node.next
            ll.remove(node)
            self.length -= 1

    # remove_last removes the last element of the list
    def remove_last(self):
        if self.length == 0:
            raise TypeError('Tried to remove empty list')
        elif self.head == self.tail:
            ll = [self.head]
            ll.remove(self.head)
            self.length -= 1
        elif self.head.next == self.tail:
            ll = [self.head, self.tail]
            ll.remove(self.tail)
            self.length -= 1
            self.head.next = None
        else:
            # initialize node to be head
            node = self.head
            while node.next != self.tail:
                node = node.next
                if node.next == self.tail:
                    ll = [self.tail]
                    ll.remove(self.tail)
                    self.length -= 1
                    self.tail = node
                    self.tail.next = None
                    break
                else:
                    pass

