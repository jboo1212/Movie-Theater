__author__ = 'Sorostitude'
import sys
from _Queue import Ticket_Line, Customer

class Ticket_Window:

    tickets = sys.maxint  # We'll keep this because it's constant throughout the instances.

    # All ticket windows start out with no customers, and no
    # knowledge of their processing time until the simulation starts
    def __init__(self, customer=None, process_time=None, current_amount_of_tickets=0):
        self.window_number = 0
        self.customer = customer
        self.process_time = process_time
        self.current_amount_of_tickets = current_amount_of_tickets

    # Increments the window number
    def increment_window_number(self):
        self.window_number += 1
        return self.window_number

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

    # Removes a customer from a window, issues them a ticket
    def remove_from_window(self):
        self.issue_ticket()
        self.customer = None

    # Canonical representation of a Ticket Window object
    def __repr__(self):

        return 'Ticket_Window({})'.format(self.customer)





