__author__ = 'Sorostitude'


from theater import Theater
import sys
from Clock import Clock
from window import Ticket_Window, Ticket_Line


class Simulation:


    def __init__(self):
        self.length_of_simulation = 0
        self.number_of_ticket_windows = 0
        self.number_of_ticket_lines = 0
        self.processing_time_for_window = []
        self.number_of_customers = []
        self.customer_arrival_time = []
        self.theater = Theater(None, None)
        self.individual_ticket_window = None




    # This takes a look at our file, 'simulation' which describes the parameters needed
    # for the simulation to run.
    def parse_file(self):
        sim = open('simulation.txt', 'r')  # open the file with 'read'
        file_list = sim.readlines()  # file_list acts as our list of lines (each line composes a list of characters)

        self.length_of_simulation = int((file_list[1])) * 60

        self.number_of_ticket_windows = int(file_list[2])

        self.number_of_ticket_lines = file_list[3]

        if self.number_of_ticket_lines == 'S':
            self.number_of_ticket_lines = 1
        else:
            self.number_of_ticket_lines = self.number_of_ticket_windows

        # 'a' was set here for the purposes of slicing; slicing
        # isn't inclusive, so 1 + 4 + self.number_of_ticket_windows
        # really is 5 + self.number_of_ticket_windows
        a = 5 + self.number_of_ticket_windows

        for n in file_list[4:a]:
            self.processing_time_for_window.append(n)

        current_position = file_list[a:]  # Look at the rest of the file
        # Storing the customers and their arrival times in a list
        for n in current_position:
            if n == 'END':
                return
            else:
                self.number_of_customers = int(n[0])
                self.customer_arrival_time = int(n[3:5])

    # Loads the appropriate information, given the data from our file
    # and runs the simulation loop.
    def run_simulation(self):

        # Read the file
        self.parse_file()

        # Make a clock object whose sole job is to track time.
        clock = Clock()

        # Set the processing times.
        self.set_processing_times()

        # Jumps the simulation forward to when customers first arrive.
        clock.time = self.customer_arrival_time

        # While the program hasn't reached the end (simulation time)...
        while clock.time != self.length_of_simulation:

                # So the logic is thus: the loop happens 'n^(simulation time - current time)' times for every window
                # Because every window needs to be checked every second.
                # Every time a customer is there, that window gets decremented via its processing time.
                # We also need a way of 'resetting the process time'
            for n in range(0, len(self.individual_ticket_window.process_time)):
                tp = self.individual_ticket_window.process_time[n]

                # If at the current time we expect customer arrivals, delegate the lines.
                if clock.time == self.customer_arrival_time:
                    self.theater.delegate_line(self.number_of_customers)
                # If there isn't a customer there, move the customer to the window.
                    if self.theater.customer_occupied_window is False:
                        self.theater.move_customer()
                # If there is a customer there, see if finished or not finished.
                    else:
                        # If the customer is finished at the window: give the former customer a ticket,
                        # remove him from the window, add the new customer to the window
                        # Reset the processing time for the 'nth' window.
                        if tp == 0:
                            self.theater.move_customer()
                            tp = self.individual_ticket_window.process_time[n]
                        else:
                            pass
                # Even if we don't expect customer arrivals, we still need to
                # check the windows.
                else:
                    if self.theater.customer_occupied_window is False:
                        self.theater.move_customer()

                    else:
                        # If the customer is finished at the window: give the former customer a ticket,
                        # remove him from the window, add the new customer to the window.
                        # Reset the processing time for the 'nth' window.
                        if tp == 0:
                            self.theater.move_customer()
                            tp = self.individual_ticket_window.process_time[n]
                        else:
                            pass

                tp -= 1

            clock.time += 1

    # NOT COMPLETE
    # Still needs to be fixed with a non-nested list implementation.
    def set_processing_times(self):
        # Initialize the theater object with the right amount of lines/windows
        self.theater = Theater(self.number_of_ticket_lines, self.number_of_ticket_windows)

        # Add the lines and the windows
        self.theater.add_lines()
        self.theater.add_windows()

        for n in range(0, len(self.theater.ticket_window_list)):
            self.individual_ticket_window = self.theater.ticket_window_list[n][0]
            self.individual_ticket_window.process_time = []
            self.individual_ticket_window.process_time = self.individual_ticket_window.process_time.append(
                                                                    self.processing_time_for_window[n])

        return self.individual_ticket_window.process_time


def main():
    simulator = Simulation()
    simulator.run_simulation()




if __name__ == "__main__":
    main()

# Object rules for changing our variables from class to attributes ----
# We don't want every simulation object to have the same information for
# different parameters
