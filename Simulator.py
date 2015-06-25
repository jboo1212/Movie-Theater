__author__ = 'Sorostitude'


from theater import Theater
from Clock import Clock



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

        self.customer_has_arrived_in_line = False

        # Window statistics
        self.number_of_tickets_sold_at_window = []

        # Figure out what to do with this.
        self.idle_time = []

        self.length_of_lines_at_the_end = 0


    # This takes a look at our file, 'simulation' which describes the parameters needed
    # for the simulation to run.
    def parse_file(self):
        sim = open('simulation.txt', 'r')  # open the file with 'read'

        file_list = sim.readlines()  # file_list acts as our list of lines (each line composes a list of characters)

        self.length_of_simulation = int((file_list[1])) * 60

        self.number_of_ticket_windows = int(file_list[2])

        self.number_of_ticket_lines = file_list[3].strip()

        if self.number_of_ticket_lines == "S":
            self.number_of_ticket_lines = 1
        else:
            self.number_of_ticket_lines = self.number_of_ticket_windows

        # There are two ticket windows, so two processing line times.
        # It still adds the newline character...
        for n in file_list[4:4+self.number_of_ticket_windows]:
            self.processing_time_for_window.append(int(n))

        # So all we care about is the 6th index and the 7th index.
        # If file_list is a list and the list contains strings...
        current_position_in_list = file_list[4+self.number_of_ticket_windows:]
        for n in current_position_in_list:
            if n == 'END':
                pass
            else:
                self.number_of_customers.append(int(n[0]))
                self.customer_arrival_time.append(int(n[2:5]))

    # Loads the appropriate information, given the data from our file
    # and runs the simulation loop.
    def run_simulation(self):

        clock = Clock()

        # Read the file.
        self.parse_file()

        # Set the processing times.
        self.set_processing_times()

        self.theater.add_lines()

        # Jumps the simulation forward to when customers first arrive.
        clock.time = self.customer_arrival_time[0]
        print "Time     %d - Simulation has started" % clock.time

        for q in range(len(self.theater.ticket_window_list)):
            self.idle_time.append(clock.time)

        # While the program hasn't reached the end (simulation time)...
        while clock.time != self.length_of_simulation + 1:

            # Loop through the windows
            for n in range(len(self.theater.ticket_window_list)):

                # Set the processing time for each window to a local variable.
                original_process_time = self.processing_time_for_window[n] - 1

                # Check for the number of lines; 1 vs. n lines
                if self.number_of_ticket_lines == 1:
                    y = 0
                else:
                    y = n

                # ISSUE:
                # Customer gets added to the wrong window.
                # This is a problem with matching index and windows inside move_customer() I think.

                # If we expect arrivals and the customer(s) haven't been added to the window yet (double-counting).

                if clock.time == self.customer_arrival_time[0] and self.customer_has_arrived_in_line is False:

                    # Move the customers to the appropriate lines
                    self.theater.delegate_line(self.number_of_customers[0])

                    self.customer_has_arrived_in_line = True

                    # For every customer, print how many have been added.
                    for q in range(self.number_of_customers[0]):
                        print "Time     %d - Customer entered line %d" % \
                              (clock.time, self.theater.ticket_line_list[y].line_number)

                    # If there is no one at the window and we can add customers to the line (length >=1),
                    # move the customer from the line to the window.
                    # 1)

                    if self.theater.ticket_window_list[n].customer_occupied_window is False:

                        self.theater.move_customer()


                        print "Time     %d - Customer exited line %d" % \
                            (clock.time, self.theater.ticket_line_list[y].line_number)
                        print "Time     %d - Customer entered window %d" % \
                            (clock.time, self.theater.ticket_window_list[n].window_number)

                        self.theater.ticket_window_list[n].process_time -= 1

                    # Given that we add customers to the line, we already prove that len >= 1;
                    # If there is someone at the window, check to see if they're done.  If
                    # they're not done, decrement the processing time for that window.
                    # 2)
                    elif self.theater.ticket_window_list[n].customer_occupied_window is True and \
                            self.theater.ticket_window_list[n].process_time != 0:

                        self.theater.ticket_window_list[n].process_time -= 1

                    # Given that we add customers to the line, we already prove that len >= 1
                    # If there is someone at the window, check to see if they're done.  If
                    # they are done, remove them from the window and add someone from line to window.
                    # Reset the processing time for that window and decrement it, since one second has passed.
                    # 3)
                    elif self.theater.ticket_window_list[n].customer_occupied_window is True and \
                            self.theater.ticket_window_list[n].process_time == 0:

                        self.theater.move_customer()

                        print "Time      %d - Customer left window %d" % \
                            (clock.time, self.theater.ticket_window_list[n].window_number)
                        print "Time      %d - Customer exited line %d" % \
                            (clock.time, self.theater.ticket_line_list[y].line_number)
                        print "Time      %d - Customer entered window %d" % \
                            (clock.time, self.theater.ticket_window_list[n].window_number)

                        self.theater.ticket_window_list[n].process_time = original_process_time
                        self.theater.ticket_window_list[n].process_time -= 1
                    # 4)
                    else:
                        self.idle_time[n] += 1

                else:
                    # 1)
                    if self.theater.ticket_window_list[n].customer_occupied_window is False and \
                            len(self.theater.ticket_line_list[y]) >= 1:

                        self.theater.move_customer()

                        print "Time     %d - Customer exited line %d" % \
                            (clock.time, self.theater.ticket_line_list[y].line_number)
                        print "Time     %d - Customer entered window %d" % \
                            (clock.time, self.theater.ticket_window_list[n].window_number)

                        self.theater.ticket_window_list[n].process_time -= 1

                    # 2)
                    elif self.theater.ticket_window_list[n].customer_occupied_window is True and \
                            self.theater.ticket_window_list[n].process_time != 0:

                        self.theater.ticket_window_list[n].process_time -= 1

                    # 3)
                    elif self.theater.ticket_window_list[n].customer_occupied_window is True and \
                            self.theater.ticket_window_list[n].process_time == 0 and \
                            len(self.theater.ticket_line_list[y]) >= 1:

                        self.theater.move_customer()
                        print "Time      %d - Customer left window %d" % \
                            (clock.time, self.theater.ticket_window_list[n].window_number)
                        print "Time      %d - Customer exited line %d" % \
                            (clock.time, self.theater.ticket_line_list[y].line_number)
                        print "Time      %d - Customer entered window %d" % \
                            (clock.time, self.theater.ticket_window_list[n].window_number)

                        self.theater.ticket_window_list[n].process_time = original_process_time

                    # 4)
                    elif self.theater.ticket_window_list[n].customer_occupied_window is True and \
                            self.theater.ticket_window_list[n].process_time == 0 and \
                            len(self.theater.ticket_line_list[y]) == 0:

                        self.theater.move_customer()
                        print "Time     %d - Customer left window %d" % \
                              (clock.time, self.theater.ticket_window_list[n].window_number)
                        self.idle_time[n] += 1
                    # 5)
                    else:
                        self.idle_time[n] += 1

                if len(self.theater.ticket_line_list[y]) >= 1 and clock.time == self.length_of_simulation:
                    self.length_of_lines_at_the_end += len(self.theater.ticket_line_list[y])
                else:
                    pass

            self.customer_has_arrived_in_line = False

            # This is a way to control iterations such that we get rid of a list element
            # once an arrival time happens.
            if clock.time == self.customer_arrival_time[0] and len(self.customer_arrival_time) >= 2:
                self.customer_arrival_time.pop(0)
                self.number_of_customers.pop(0)
            else:
                pass

            # Increment the time after we check all the windows.

            clock.time += 1
            
    def set_processing_times(self):
        # Initialize the theater object with the right amount of lines/windows
        self.theater = Theater(self.number_of_ticket_lines, self.number_of_ticket_windows)

        # Add the lines and the windows
        self.theater.add_windows()

        for n in range(len(self.theater.ticket_window_list)):
            # For every ticket window we have, set the processing
            # time equivalent to the processing time attribute that Windows have.
            self.theater.ticket_window_list[n].process_time = self.processing_time_for_window[n]

        return self.theater.ticket_window_list

    def statistics_for_simulation(self):

        # Window loop
        for a in range(len(self.theater.ticket_window_list)):

            self.number_of_tickets_sold_at_window.append(
                self.theater.ticket_window_list[a].tickets_sold())

            print "Window %d" % self.theater.ticket_window_list[a].window_number
            print "Tickets sold: %d" % self.number_of_tickets_sold_at_window[a]
            print "Idle time: %.0f%%" % (100 * (float(self.idle_time[a]) / self.length_of_simulation))

        for x in range(len(self.theater.ticket_line_list)):
            print "Line %d" % self.theater.ticket_line_list[x].line_number

        print "Customers waiting at simulation end: %d" % self.length_of_lines_at_the_end



def main():
    simulation = Simulation()
    simulation.run_simulation()

    simulation.statistics_for_simulation()


if __name__ == "__main__":
    main()

