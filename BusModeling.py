class DukeBusSystem:
    def __init__(self, id, time_between_ew, time_stop_along_route, let_off_people, pull_up_to_stop, wait_at_stop_for_people, num_buses, num_people_running, num_people_on_bus, num_stops=1, time_takes_to_wait_for_them=45/60):
        self.id = id
        self.time_between_ew = time_between_ew
        self.time_stop_along_route = time_stop_along_route
        self.let_off_people = let_off_people
        self.pull_up_to_stop = pull_up_to_stop
        self.wait_at_stop_for_people = wait_at_stop_for_people
        self.num_buses = num_buses
        
        # Parameters for simulation
        self.num_stops = num_stops
        self.num_people_running = num_people_running
        self.num_people_on_bus = num_people_on_bus
        self.time_takes_to_wait_for_stragglers = time_takes_to_wait_for_them

        # Printing the parameters passed to the class
        print(f"Duke Bus System ({self.id}) Parameters:")
        print("-" * 40)
        print(f"Time Between East and West: {self.time_between_ew} minutes")
        print(f"Time Per Stop Along Route: {self.time_stop_along_route} minutes")
        print(f"Number of Stops Along Route: {self.num_stops}")
        print(f"Time to Let Off People: {self.let_off_people} minutes")
        print(f"Time to Pull Up to Stop: {self.pull_up_to_stop} minutes")
        print(f"Wait Time at Stop for People: {self.wait_at_stop_for_people} minutes")
        print(f"Number of Buses: {self.num_buses}")
        print("-" * 40)

    def get_one_way_time(self):
        return self.time_between_ew + (self.num_stops * self.time_stop_along_route) + self.let_off_people + self.pull_up_to_stop + self.wait_at_stop_for_people

    def get_lap_time(self, one_way_time):
        return one_way_time * 2

    def get_optimized_bus_mirror_time(self, lap_time):
        return lap_time / self.num_buses

    def get_average_wait_time_uniform(self, bus_mirror_time):
        return (bus_mirror_time / (bus_mirror_time + self.wait_at_stop_for_people) * (bus_mirror_time / 2)) + (self.wait_at_stop_for_people / (bus_mirror_time + self.wait_at_stop_for_people) * (self.wait_at_stop_for_people / 2))

    def get_wait_time_benefit_of_letting_late_people_on_bus(self, bus_mirror_time):
        running_time_saved_per_person = bus_mirror_time - self.time_takes_to_wait_for_stragglers
        people_on_bus_time_wasted = self.time_takes_to_wait_for_stragglers
        wait_time_saved_total = -((self.num_people_on_bus * people_on_bus_time_wasted) - (self.num_people_running * running_time_saved_per_person))
        return wait_time_saved_total / (self.num_people_on_bus + self.num_people_running)

    def get_new_average_wait_time(self, wait_time_saved_per_person, average_wait_time):
        return average_wait_time - wait_time_saved_per_person

    def simulate(self):
        one_way_time = self.get_one_way_time()
        lap_time = self.get_lap_time(one_way_time)
        bus_mirror_time = self.get_optimized_bus_mirror_time(lap_time)
        average_wait_time = self.get_average_wait_time_uniform(bus_mirror_time)
        wait_time_saved_per_person = self.get_wait_time_benefit_of_letting_late_people_on_bus(bus_mirror_time)
        new_average_wait_time = self.get_new_average_wait_time(wait_time_saved_per_person, average_wait_time)
        
        # Printing the results
        print(f"Duke Bus System ({self.id}) Simulation Results:")
        print("-" * 40)
        print(f"One Way Time: {one_way_time:.2f} minutes")
        print(f"Lap Time (Round Trip): {lap_time:.2f} minutes")
        print(f"Optimized Bus Offset: {bus_mirror_time:.2f} minutes")
        print(f"Max Wait Time: {bus_mirror_time:.2f} minutes")
        print(f"Average Wait Time Per Person (Uniform Distribution): {average_wait_time:.2f} minutes")
        print(f"Scenario 1: {self.num_people_running} people are running up to a bus with {self.num_people_on_bus} people. What would be the effect of waiting {self.time_takes_to_wait_for_stragglers*60} seconds to let them on?")
        print(f"Wait Time Saved Per Person: {wait_time_saved_per_person:.2f} minutes")
        print(f"New Average Wait Time: {new_average_wait_time:.2f} minutes")
        print("-" * 40)

#Object Creation
duke_system = DukeBusSystem(1, time_between_ew=7, time_stop_along_route=20/60, let_off_people=30/60, pull_up_to_stop=15/60, wait_at_stop_for_people=5, num_buses=3, num_people_running=3, num_people_on_bus=40, num_stops=1, time_takes_to_wait_for_them=45/60)
duke_system.simulate()
duke_system = DukeBusSystem(2, time_between_ew=7, time_stop_along_route=20/60, let_off_people=30/60, pull_up_to_stop=15/60, wait_at_stop_for_people=0.5, num_buses=5, num_people_running=3, num_people_on_bus=40, num_stops=1, time_takes_to_wait_for_them=45/60)
duke_system.simulate()
