__author__ = 'Sorostitude'

from _Queue import Ticket_Line, Customer
from window import Ticket_Window


class Theater:

    # In order to 'act' as a Theater and to manage the lines/windows,
    # our object needs to know how many lines/windows we pass in.
    def __init__(self, num_of_lines, num_of_windows):
        self.ticket_line_list = []
        self.ticket_window_list = []

        self.num_of_lines = num_of_lines
        self.num_of_windows = num_of_windows

        self.customer = None

    # Creates 'n' amount of ticket windows and gives them numbers.
    # Ticket Window(1), Ticket Window(2),...
    # with no notion of a customer and how long it takes to process a customer
    def add_windows(self):

        for n in range(self.num_of_windows):
            ticket_window = Ticket_Window()
            self.ticket_window_list.append(ticket_window)
            self.ticket_window_list[n].window_number = n+1


        return self.ticket_window_list

    # Creates 'n' amount of ticket lines and gives them numbers.
    # Ticket Line(1), Ticket Line(2)...
    def add_lines(self):

        for n in range(self.num_of_lines):
            ticket_line = Ticket_Line()

            # Add a ticket line to a list of ticket lines.
            self.ticket_line_list.append(ticket_line)
            # Each ticket line gets its own number.
            self.ticket_line_list[n].line_number += n+1

        return self.ticket_line_list

    # Delegates the lines ONLY - does not move customers to the windows.
    # If there is one line, we only need to add customers to the single line
    # If there is more than one line, we need to make sure customers are going
    # to the line with the lowest amount of customers there.
    def delegate_line(self, num_of_customers):

        if self.num_of_lines < self.num_of_windows:

            a = self.ticket_line_list[0]

            for n in range(num_of_customers):

                # Creates a customer object
                customer = Customer()

                # Queue the customer
                a.enqueue(customer)

        elif self.num_of_lines == self.num_of_windows:

            min_number = 9000
            min_index_number = 0

            for x in range(num_of_customers):

                customer = Customer()

                for n in range(len(self.ticket_line_list)):

                    if len(self.ticket_line_list[n]) <= min_number:

                        min_number = len(self.ticket_line_list[n])

                        min_index_number = n

                    else:
                        # If the length of the current ticket line is bigger than
                        # the min number, we know to queue to the previous line.
                        min_index_number = n - 1

                        min_number = len(self.ticket_line_list[n])

                self.ticket_line_list[min_index_number].enqueue(customer)

        else:
            pass

        return self.ticket_line_list

    def move_customer(self):

        for n in range(len(self.ticket_line_list)):
            for x in range(len(self.ticket_window_list)):
                current_ticket_line = self.ticket_line_list[n]
                current_window = self.ticket_window_list[x]

                # n lines, n windows
                if self.num_of_lines == self.num_of_windows and n == x:

                    # Case 1:
                    # If there is no customer at the window and there is at least one person in the same line.
                    # Case 2:
                    # If the customer has occupied the window for enough time, get rid of him.
                    # Case 3:
                    # If there is no customer at the window and there is no one in line and the customer is done,
                    # get rid of him.
                    if current_window.customer is None and len(current_ticket_line) >= 1:
                        current_ticket_line.dequeue()
                        current_window.add_customer_to_window()

                    elif not (current_window.customer is None) and len(current_ticket_line) >= 1 and \
                            current_window.process_time == 0:

                        current_window.remove_from_window()
                        current_ticket_line.dequeue()
                        current_window.add_customer_to_window()

                    elif not (current_window.customer is None) and len(current_ticket_line) == 0 and \
                            current_window.process_time == 0:

                        current_window.remove_from_window()
                    else:
                        pass

                # 1 line, n windows
                elif self.num_of_lines < self.num_of_windows:
                    # Case 1:
                    # If there is no customer at the window and there is at least one person in the same line.
                    # Case 2:
                    # If the customer has occupied the window for enough time, get rid of him.
                    # Case 3:
                    # If there is no customer at the window and there is no one in line and the customer is done,
                    # get rid of him.
                    if current_window.customer is None and len(current_ticket_line) >= 1:
                        current_ticket_line.dequeue()
                        current_window.add_customer_to_window()

                    elif not (current_window.customer is None) and len(current_ticket_line) >= 1 and \
                            current_window.process_time == 0:

                        current_window.remove_from_window()
                        current_ticket_line.dequeue()
                        current_window.add_customer_to_window()

                    elif not (current_window.customer is None) and len(current_ticket_line) == 0 and \
                            current_window.process_time == 0:

                        current_window.remove_from_window()
                    else:
                        pass

                else:
                    pass

        return self.ticket_window_list, self.ticket_line_list

    # Make a custom representation for a Theater object.
    def __repr__(self):
        return '{}: {} \n {}]'.format(self.__class__.__name__,
                                      self.ticket_line_list,
                                      self.ticket_window_list)


# Let's see if delegate lines is working properly; it IS NOT WORKING PROPERLY
# A customer gets moved to Ticket Line 2, not Ticket Line 1.
# The fact still remains that if both lines are the same length, neither one is THE minimum line.
# We need to say, put the customer in the line with the shortest line number.

theater = Theater(2, 2)
theater.add_lines()
theater.add_windows()

theater.delegate_line(1)

print len(theater.ticket_line_list[1])
