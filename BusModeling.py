import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class DukeBusSystem:
    def __init__(self, id, time_between_ew, time_stop_along_route, let_off_people, pull_up_to_stop, wait_at_stop_for_people, num_buses, num_people_running, num_people_on_bus, print_output=True, capacity = 100, num_stops=2, time_takes_to_wait_for_them=45/60):
        self.id = id
        self.time_between_ew = time_between_ew
        self.time_stop_along_route = time_stop_along_route
        self.let_off_people = let_off_people
        self.pull_up_to_stop = pull_up_to_stop
        self.wait_at_stop_for_people = wait_at_stop_for_people
        self.num_buses = num_buses
        self.print_output = print_output
        self.num_stops = num_stops
        self.num_people_running = num_people_running
        self.num_people_on_bus = num_people_on_bus
        self.time_takes_to_wait_for_stragglers = time_takes_to_wait_for_them
        self.capacity = capacity

        self.one_way_time = None
        self.lap_time = None
        self.bus_mirror_time = None
        self.average_wait_time = None
        self.wait_time_saved_per_person = None
        self.new_average_wait_time = None
        self.throughput = None


    def get_average_time_person_on_bus(self):
        return self.average_wait_time+self.get_true_ew_time()

    def get_true_ew_time(self):
        return self.get_one_way_time()-self.wait_at_stop_for_people
    
    def get_one_way_time(self):
        return self.time_between_ew + (self.num_stops * self.time_stop_along_route) + self.let_off_people + self.pull_up_to_stop + self.wait_at_stop_for_people

    def get_max_hourly_throughput(self):
        return ((self.capacity)*self.num_buses)*60/self.get_one_way_time()

    def get_lap_time(self, one_way_time):
        return one_way_time * 2

    def get_optimized_bus_mirror_time(self, lap_time):
        return lap_time / self.num_buses
    
    def get_unoptimized_average_wait_time(self,lap_time):
        if self.get_nonoptimized_bus_mirror_time() == "Error": return "Error"
        mirror_array = self.get_nonoptimized_bus_mirror_time()
        wt_1to2 = mirror_array[0]
        wt_2to3 = mirror_array[1]
        wt_3to4 = mirror_array[2]
        wt_4to1 = lap_time - wt_1to2-wt_2to3-wt_3to4
        percent_people_between_1to2= wt_1to2/lap_time
        percent_people_between_2to3= wt_2to3/lap_time
        percent_people_between_3to4= wt_3to4/lap_time
        percent_people_between_4to1= wt_4to1/lap_time

        weighted_average_wait_times = wt_1to2*percent_people_between_1to2+wt_2to3*percent_people_between_2to3+wt_3to4*percent_people_between_3to4+wt_4to1*percent_people_between_4to1
        return weighted_average_wait_times
    
    def get_nonoptimized_bus_mirror_time(self):
            #Depiction of horribly optimized bus system
            if self.num_buses !=4: return "Error" #"Error, Duke Bus system primarily runs with 4 (or 5) buses. This method is intended to represent what the Duke bus system can sometimes look like, and thus incompatible with all numbers of buses."
            offsets = [0.25, 0.25, 2+self.wait_at_stop_for_people]
            return offsets
    def get_unoptimized_max_wait_time(self, lap_time):
        if self.get_nonoptimized_bus_mirror_time() == 0: return 0
        mirror_array = self.get_nonoptimized_bus_mirror_time()
        wt_1to2 = mirror_array[0]
        wt_2to3 = mirror_array[1]
        wt_3to4 = mirror_array[2]
        wt_4to1 = lap_time - wt_1to2-wt_2to3-wt_3to4
        return wt_4to1 

    def get_average_wait_time_uniform(self, bus_mirror_time):
        return bus_mirror_time/2
        #return (bus_mirror_time / (bus_mirror_time + self.wait_at_stop_for_people) * (bus_mirror_time / 2)) + (self.wait_at_stop_for_people / (bus_mirror_time + self.wait_at_stop_for_people) * (self.wait_at_stop_for_people / 2))

    def get_max_wait_time(self):
        one_way_time = self.get_one_way_time()
        lap_time = self.get_lap_time(one_way_time)
        return self.get_optimized_bus_mirror_time(lap_time)
    
    def get_wait_time_benefit_of_letting_late_people_on_bus(self, bus_mirror_time):
        running_time_saved_per_person = bus_mirror_time - self.time_takes_to_wait_for_stragglers
        people_on_bus_time_wasted = self.time_takes_to_wait_for_stragglers
        wait_time_saved_total = -((self.num_people_on_bus * people_on_bus_time_wasted) - (self.num_people_running * running_time_saved_per_person))
        return wait_time_saved_total / (self.num_people_on_bus + self.num_people_running)

    def get_new_average_wait_time(self, wait_time_saved_per_person, average_wait_time):
        return average_wait_time - wait_time_saved_per_person

    def simulate(self):
        one_way_time = self.get_one_way_time()
        self.one_way_time = one_way_time
        lap_time = self.get_lap_time(one_way_time)
        self.lap_time = lap_time
        bus_mirror_time = self.get_optimized_bus_mirror_time(lap_time)
        self.bus_mirror_time = bus_mirror_time
        average_wait_time = self.get_average_wait_time_uniform(bus_mirror_time)
        self.average_wait_time = average_wait_time
        wait_time_saved_per_person = self.get_wait_time_benefit_of_letting_late_people_on_bus(bus_mirror_time)
        self.wait_time_saved_per_person = wait_time_saved_per_person
        new_average_wait_time = self.get_new_average_wait_time(wait_time_saved_per_person, average_wait_time)
        self.new_average_wait_time = new_average_wait_time
        throughput = self.get_max_hourly_throughput()
        self.throughput = throughput
        
        # Storing the results
        self.results = {
            "One Way Time": one_way_time,
            "Lap Time (Round Trip)": lap_time,
            "Optimized Bus Offset": bus_mirror_time,
            "Max Wait Time": bus_mirror_time,
            "Average Wait Time Per Person (Uniform Distribution)": average_wait_time,
            "New Average Wait Time": new_average_wait_time
        }

        # Printing the parameters and results if requested
        if self.print_output:
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
            
            # Printing the results
            print(f"Duke Bus System ({self.id}) Simulation Results:")
            print("-" * 40)
            print(f"One Way Time: {one_way_time:.2f} minutes")
            print(f"Lap Time (Round Trip): {lap_time:.2f} minutes")
            print(f"Optimized Bus Offset: {bus_mirror_time:.2f} minutes")
            print(f"Max Wait Time: {bus_mirror_time:.2f} minutes")
            print(f"Average Wait Time Per Person (Uniform Distribution): {average_wait_time:.2f} minutes")
            print(f"Maximum Throughput Per Hour: {throughput:.0f} people")
            if self.id == "Actual" and self.num_buses == 4:
                print(f"Scenario: The Duke Bus System often has buses driving right behind other buses. If this was the case with four buses, three running close to each other and one properly spread out, what would the max and average wait time be?")
                max_wait_unop = self.get_unoptimized_max_wait_time(self.get_lap_time(self.get_one_way_time()))
                average_wait_unop = self.get_unoptimized_average_wait_time(self.get_lap_time(self.get_one_way_time()))
                print(f"Max Wait Time: {max_wait_unop:.2f} minutes")
                print(f"Average Wait Time Per Person: {average_wait_unop:.2f} minutes")
            
            print(f"Scenario: {self.num_people_running} people are running up to a bus with {self.num_people_on_bus} people. What would be the effect of waiting {self.time_takes_to_wait_for_stragglers*60} seconds to let them on?")
            print(f"Wait Time Saved Per Person: {wait_time_saved_per_person:.2f} minutes")
            print(f"New Average Wait Time: {new_average_wait_time:.2f} minutes")
            print("-" * 40)
        
        return self.results

def simulate_for_params(wait_times, bus_numbers, time_between_ew=7, time_stop_along_route=20/60, let_off_people=30/60, pull_up_to_stop=15/60, num_people_running=3, num_people_on_bus=40, print_output=False, num_stops=2, time_takes_to_wait_for_them=45/60):
    results = {}
    for wait_time in wait_times:
        for bus_num in bus_numbers:
            duke_system = DukeBusSystem(
                id=f"wait_time={wait_time}, bus_num={bus_num}", 
                time_between_ew=time_between_ew, 
                time_stop_along_route=time_stop_along_route, 
                let_off_people=let_off_people, 
                pull_up_to_stop=pull_up_to_stop, 
                wait_at_stop_for_people=wait_time, 
                num_buses=bus_num, 
                num_people_running=num_people_running, 
                num_people_on_bus=num_people_on_bus, 
                print_output=print_output,
                num_stops=num_stops, 
                time_takes_to_wait_for_them=time_takes_to_wait_for_them
            )
            sim_result = duke_system.simulate()
            results[(wait_time, bus_num)] = sim_result["Average Wait Time Per Person (Uniform Distribution)"]
    return results

if __name__ == "__main__":
    # Running the simulations
    wait_times = np.linspace(0.5, 8, 16)  # 16 values between 0.5 and 16
    bus_numbers = np.linspace(1, 10, 10, dtype=int)  # (10) Integer values between 1 and 10
    results_with_output = simulate_for_params(wait_times, bus_numbers)

    # Extracting results for graphing
    X, Y, Z = [], [], []
    for (wait_time, bus_num), avg_wait in results_with_output.items():
        X.append(wait_time)
        Y.append(bus_num)
        Z.append(avg_wait)


    # Convert the results to a DataFrame for heatmap
    df = pd.DataFrame({
        'Wait Time at Stop': X,
        'Number of Buses': Y,
        'Average Wait Time (Uniform Distribution)': Z
    })

    # Create a pivot table for the heatmap
    heatmap_data = df.pivot_table(index='Number of Buses', columns='Wait Time at Stop', values='Average Wait Time (Uniform Distribution)')

    # Plot the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap='cividis', linewidths=.5)
    plt.title('Effects of Wait Time at Stop and Number of Buses on Average Wait Time (Uniform Distribution)')
    plt.show()

    #Object creation for simulation
    duke_actual_system = DukeBusSystem("Actual", time_between_ew=5.5, time_stop_along_route=20/60, let_off_people=20/60, pull_up_to_stop=20/60, wait_at_stop_for_people=4.2, num_buses=4, num_people_running=3, num_people_on_bus=40, print_output=True, capacity = round((112+66*3)/4,0), num_stops=2, time_takes_to_wait_for_them=45/60)
    duke_actual_system.simulate()
    print(duke_actual_system.get_max_hourly_throughput())
    duke_optimized_system = DukeBusSystem("Optimized", time_between_ew=5.5, time_stop_along_route=20/60, let_off_people=20/60, pull_up_to_stop=20/60, wait_at_stop_for_people=45/60, num_buses=4, num_people_running=3, num_people_on_bus=40, print_output=True, capacity = round((112+66*3)/4,0), num_stops=2, time_takes_to_wait_for_them=45/60)
    duke_optimized_system.simulate()

class Student:
    def __init__(self, time_allocated_for_bus=15):
        self.time_allocated_for_bus = time_allocated_for_bus

    def probability_of_being_late(self, bus_system, want_output=True):
        average_wait = bus_system.get_average_wait_time_uniform(bus_system.get_optimized_bus_mirror_time(bus_system.get_lap_time(bus_system.get_one_way_time())))
        max_wait = bus_system.get_max_wait_time()
        true_ew = bus_system.get_true_ew_time()
        
        # If average wait time is less than the time left to reach class after waiting, then the student will surely be on time.
        if max_wait < self.time_allocated_for_bus-true_ew:
            self.probability = 0
        # If the max wait time is less than the time left to reach class after waiting, then the student has a perfect chance in theory of being on time.
        elif self.time_allocated_for_bus < true_ew:
            self.probability = 1
        else:
            self.probability = 1-(self.time_allocated_for_bus-true_ew)/bus_system.get_max_wait_time()
        if want_output:
            self.do_output(self.probability, bus_system)

        return self.probability
    
    def do_output(self, probability, bus_system):
        print(f"A student that allocates {self.time_allocated_for_bus} minutes for the ({bus_system.id}) bus system will be late approximately {probability*100:.2f}% of the time.")

def visualize_probabilities(duke_system1, duke_system2):
    # Calculate the probabilities
    times = np.arange(5, 21.25, 0.25).tolist() #Get probability every 0.25 minutes starting at 5 minutes and ending at 21.25
    probabilities1 = [Student(time).probability_of_being_late(duke_system1, want_output=False) for time in times]
    probabilities2 = [Student(time).probability_of_being_late(duke_system2, want_output=False) for time in times]

    # Plot the results
    plt.figure(figsize=(10, 6)) #Aspect ratio
    
    # Plotting for duke_system1
    plt.plot(times, probabilities1, marker=None, linewidth=3, color='orange', label=f'Duke System {duke_system1.id}')
    
    # Plotting for duke_system2
    plt.plot(times, probabilities2, marker=None, linewidth=3, color='blue', label=f'Duke System {duke_system2.id}')
    
    plt.xlabel('Time Allocated for Bus (minutes)')
    plt.ylabel('Probability of Being Late')
    plt.title('Probability of Being Late vs Time Allocated for Bus')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__": 
    visualize_probabilities(duke_actual_system, duke_optimized_system)
    # Create Student instances
    student_actual = Student(time_allocated_for_bus=10)
    student_actual.probability_of_being_late(duke_actual_system, want_output=True)
    student_hopeful = Student(time_allocated_for_bus=10)
    student_hopeful.probability_of_being_late(duke_optimized_system, want_output=True)

