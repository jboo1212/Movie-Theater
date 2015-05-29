__author__ = 'Sorostitude'

from _Queue import Ticket_Line, Customer
from window import Ticket_Window
from Clock import Clock


class Theater:

    # In order to 'act' as a Theater and to manage the lines/windows,
    # our object needs to know how many lines/windows we pass in.
    def __init__(self, num_of_lines, num_of_windows):
        self.ticket_line_list = []
        self.ticket_window_list = []

        self.num_of_lines = num_of_lines
        self.num_of_windows = num_of_windows

        self.customer_occupied_window = False
        self.customer = None

    # Creates 'n' amount of ticket windows and gives them numbers.
    # (Ticket Window, 1), (Ticket Window, 2)...
    # with no notion of a customer and how long it takes to process a customer
    # More details in ICS 33 'No Line on the Horizon' Documentation.
    def add_windows(self):

        for n in range(self.num_of_windows):
            ticket_window = Ticket_Window()
            self.ticket_window_list.append(ticket_window)

        return self.ticket_window_list

    # Creates 'n' amount of ticket lines and gives them numbers.
    # (Ticket Line, 1), (Ticket Line, 2)...
    def add_lines(self):

        for n in range(self.num_of_lines):
            ticket_line = Ticket_Line()
            self.ticket_line_list.append(ticket_line)

        return self.ticket_line_list

    # Delegates the lines ONLY - does not move customers to the windows.
    # If there is one line, we only need to add customers to the single line
    # If there is more than one line, we need to make sure customers are going
    # to the line with the lowest amount of customers there.
    def delegate_line(self, num_of_customers):

        self.add_lines()

        if self.num_of_lines < self.num_of_windows:

            a = self.ticket_line_list[0]

            for n in range(num_of_customers):

                # Creates a customer object
                customer = Customer()

                # Queue the customer
                a.enqueue(customer)

        elif self.num_of_lines == self.num_of_windows:

            for x in range(num_of_customers):

                customer = Customer()

                # Make a customer and whatever line has
                # the lowest number of people in it, given that
                # there are all equal amount of people in the lines,
                # put the customer in the lowest number line.
                if len(self.ticket_line_list[0]) == len(self.ticket_line_list[1]):

                    self.ticket_line_list[0].enqueue(customer)

                else:
                    self.ticket_line_list[x].enqueue(customer)

        return self.ticket_line_list

    # Takes a customer from a line to a window;
    # There are two cases ------
    # 1) Customer isn't there at the window AND can be added to the window (i.e. in the line)
    # Customer must also be at his designated window (line 1 >> window 1, line 2 >> window 2)...
    # 2) Customer has been at the window for the designated amount of time so he must be given
    # his ticket and removed from the window.
    def move_customer(self):

        for window_element in self.ticket_window_list:
            for line_element in self.ticket_line_list:
                ticket_window = window_element[0]
                ticket_line = line_element[0]
                if (ticket_window.customer is None and not ticket_line.front() is None and
                    window_element[1] == line_element[1]):

                    ticket_line.dequeue()
                    ticket_window.add_customer_to_window()
                    self.customer_occupied_window = True

                else:
                    ticket_window.remove_from_window()
                    ticket_line.dequeue()
                    ticket_window.add_customer_to_window()
                    self.customer_occupied_window = True

            return self.customer_occupied_window

    # Make a custom representation for a Theater object.
    def __repr__(self):
        return '{}: {} \n {}]'.format(self.__class__.__name__,
                                      self.ticket_line_list,
                                      self.ticket_window_list)



# NOT COMPLETE;
# Buggy --- 
theater = Theater(2, 0)
theater.delegate_line(1)
print len(theater.ticket_line_list[0])






