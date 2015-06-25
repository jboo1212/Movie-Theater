__author__ = 'Sorostitude'
import sys
from _Queue import Ticket_Line, Customer

class Ticket_Window:

    tickets = sys.maxint  # We'll keep this because it's constant throughout the instances.

    # All ticket windows start out with no customers, and no
    # knowledge of their processing time until the simulation starts
    def __init__(self, current_amount_of_tickets=0):
        self.window_number = 0
        self.customer = None

        self.process_time = 0
        self.current_amount_of_tickets = current_amount_of_tickets

        self.customer_occupied_window = False

    # Gives a ticket to the customers by decrementing how many tickets there are
    def issue_ticket(self):
        if self.current_amount_of_tickets == 0:
            self.current_amount_of_tickets = self.tickets - 1
        else:
            self.current_amount_of_tickets -= 1
        return self.current_amount_of_tickets

    # Returns how many tickets are sold from the original amount in that window
    def tickets_sold(self):
        sold_tickets = self.tickets - self.current_amount_of_tickets
        return sold_tickets

    # Adds a customer to a window
    def add_customer_to_window(self):
        self.customer = Customer()
        self.customer_occupied_window = True

    # Removes a customer from a window, issues them a ticket
    def remove_from_window(self):
        self.issue_ticket()
        self.customer = None
        self.customer_occupied_window = False

    # Canonical representation of a Ticket Window object
    def __repr__(self):

        return 'Ticket_Window({})'.format(self.process_time)


