from data_classes import read_data, Solution, Vehicle
import turtle
import math
import time
import random
import copy
def main():
    data_file = 'data.json'
    vehicles, packages = read_data(data_file)
   
    best_sol, history = run_genetic_algorithm( vehicles, packages, population_size=6, mutation_rate=0.1, generations=500)
    
    print("=== Best Solution ===")
    print(f"Fitness: {best_sol.fit}")
    print(f"Total distance: {best_sol.calculate_distance():.2f}")
    for v_idx, vehicle in enumerate(best_sol.vehicles, 1):
        print(f" Vehicle {v_idx}: load {vehicle.current_capacity}/{vehicle.max_capacity}")
    print("History (first,last):", history[0], "...", history[-1])


    draw(best_sol)
    

    
def draw(best_sol):
    # Constants
    SCALE        = 5              # 1 km = 5 pixels
    MOVE_PIXELS  = 5        # car jump per animation frame
    FRAME_DELAY  = 0.01           # pause between frames
    PANEL        = 35 * SCALE     # side panel width in pixels

    # Setup screen with extra right-side space
    MAP_W, MAP_H = 100 * SCALE, 100 * SCALE
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.title("Vehicle Delivery Routes")
    screen.setworldcoordinates(0, 0, MAP_W + PANEL, MAP_H)
    screen.tracer(0, 0)

    # Draw title
    title = turtle.Turtle(visible=False)
    title.penup()
    title.color("white")
    title.goto(MAP_W / 2, MAP_H - 10)
    title.write("Vehicle Delivery Routes", align="center", font=("Arial", 16, "bold"))

    # Draw right-hand panel background (optional white)
    panel_bg = turtle.Turtle(visible=False)
    panel_bg.penup()
    panel_bg.color("white")
    panel_bg.goto(MAP_W, 0)
    panel_bg.begin_fill()
    for _ in range(2):
        panel_bg.forward(PANEL)
        panel_bg.left(90)
        panel_bg.forward(MAP_H)
        panel_bg.left(90)
    panel_bg.end_fill()

    # Register custom car shape
    car_coords = [(-10, 0), (-10, 5), (-7, 10), (7, 10),
                (10, 5), (10, 0), (7, -3), (7, 0),
                (-7, 0), (-7, -3)]
    car_shape = turtle.Shape("polygon", car_coords)
    screen.register_shape("car", car_shape)

    # Draw all house locations
    house = turtle.Turtle(visible=False)
    house.penup()
    house.color("pink")
    house.shape("square")

    for v in best_sol.vehicles:
        for pkg in v.packages:
            x, y = pkg.destination
            house.goto(x * SCALE, y * SCALE)
            house.stamp()
            house.goto(x * SCALE + 5, y * SCALE + 5)
            house.write(f"{pkg.weight}kg", font=("Arial", 10, "normal"))

    # Red dot marker for delivered stops
    marker = turtle.Turtle(visible=False)
    marker.penup()
    marker.shape("circle")
    marker.color("red")

    # Car turtles
    cars = []
    colors = ["blue", "green", "red", "purple", "orange", "yellow", "cyan", "magenta"]

    for idx, v in enumerate(best_sol.vehicles):
        car = turtle.Turtle(shape="car")
        car.penup()
        car.setheading(90)
        car.color(colors[idx % len(colors)])
        car.speed(0)
        cars.append(car)

    # Animate car movement
    depot_x, depot_y = 0 * SCALE, 0 * SCALE

    for car, vehicle in zip(cars, best_sol.vehicles):
        car.goto(depot_x, depot_y)

        for pkg in vehicle.packages:
            tx, ty = pkg.destination[0] * SCALE, pkg.destination[1] * SCALE
            dx, dy = tx - car.xcor(), ty - car.ycor()
            dist   = math.hypot(dx, dy)

            steps = max(int(dist / MOVE_PIXELS), 1)
            step_x, step_y = dx / steps, dy / steps

            for _ in range(steps):
                car.goto(car.xcor() + step_x, car.ycor() + step_y)
                screen.update()
                time.sleep(FRAME_DELAY)

            car.goto(tx, ty)
            marker.goto(tx, ty)
            marker.stamp()
            screen.update()
            time.sleep(FRAME_DELAY)

        # Return to depot
        car.goto(depot_x, depot_y)
        marker.goto(depot_x, depot_y)
        marker.stamp()
        screen.update()
        time.sleep(FRAME_DELAY)

    # Draw right-side vehicle stats
    writer = turtle.Turtle(visible=False)
    writer.penup()
    writer.color("black")

    cx = MAP_W + PANEL / 2
    cy = MAP_H - 70
    writer.goto(cx, cy)
    writer.write(f"\nTotal distance:\n{best_sol.calculate_distance():.2f} km\n\n",
                align="center", font=("Arial", 12, "bold"))
    
    for i, v in enumerate(best_sol.vehicles, 1):
        writer.goto(cx, cy - 25 * i)
       
        writer.write(f"V{i}: {v.current_capacity}/{v.max_capacity} kg",
                    align="center", font=("Arial", 12, "normal"))

    screen.update()
    screen.exitonclick()


def run_genetic_algorithm(vehicles, packages,population_size=50,mutation_rate=0.05,  generations=500):
  

    solutions=population(vehicles,packages,population_size)
    best_history = []
    for gen in range(1, generations+1):
        sorted_solutions=fitness_sorting(solutions)
        best_history.append(sorted_solutions[0].fit)
        elite_count = 2
        elites = sorted_solutions[:elite_count]
        needed = population_size - elite_count
        final=selection(needed,sorted_solutions)
        parent=parents(final,needed)
    
        parent_pair=pairs(parent)
        crossoveres=crossover(parent_pair)
    
        mutation=mutaion(crossoveres,mutation_rate)
        offspring_sorted = fitness_sorting(mutation)

        
        solutions = elites + offspring_sorted
    final_sorted = fitness_sorting(solutions)
    return final_sorted[0], best_history
def mutaion(solutions,mutation_rate):
    for solution in solutions:
        mutate(solution,mutation_rate)
    return solutions
def mutate(solution,mutation_rate):
    vehicles = solution.vehicles
    number = random.random()
    if number < mutation_rate:
        print("mutaion happened!")
        v1, v2 = random.sample(vehicles, 2)
        if not v1.packages or not v2.packages:
             print("vhecals have no packages!")
             return

        p1 = random.choice(v1.packages)
        p2 = random.choice([p for p in v2.packages if p.uid != p1.uid])
        new_v1_weight = v1.current_capacity - p1.weight + p2.weight
        new_v2_weight = v2.current_capacity - p2.weight + p1.weight
        if new_v1_weight <= v1.max_capacity and new_v2_weight <= v2.max_capacity:
            for pkg in v1.packages:
                    x, y = pkg.destination
 
                    print(f" van1:  ({x}, {y}) | {pkg.weight}kg | Priority {pkg.priority}")
            for pkg in v2.packages:
                    x, y = pkg.destination
 
                    print(f" van2  ({x}, {y}) | {pkg.weight}kg | Priority {pkg.priority}")
            
            v1.packages.remove(p1)
            v2.packages.remove(p2)

            v1.packages.append(p2)
            v2.packages.append(p1)
            v1.current_capacity = new_v1_weight
            v2.current_capacity = new_v2_weight
            for pkg in v1.packages:
                    x, y = pkg.destination
 
                    print(f"van1   ({x}, {y}) | {pkg.weight}kg | Priority {pkg.priority}")
            for pkg in v2.packages:
                    x, y = pkg.destination
 
                    print(f" van2  ({x}, {y}) | {pkg.weight}kg | Priority {pkg.priority}")
            

def fitness_sorting(solutions):
    for solution in solutions:
        solution.fitness()
    sorted_solutions=sorted(solutions, key=lambda solution: solution.fit, reverse=True)
    i=1
    for solution in sorted_solutions:
        solution.set_rank(i)
        i=i+1
    return sorted_solutions

def crossover(parent_pairs):
    crossovers = []

    for parent1, parent2 in parent_pairs:
        # Child 1: parent1 dominant
        child1 = build_child_from_parents(parent1, parent2)
        crossovers.append(child1)

        # Child 2: parent2 dominant
        child2 = build_child_from_parents(parent2, parent1)
        crossovers.append(child2)

    return crossovers


def build_child_from_parents(p1,p2):
    """Create a child solution by greedily placing packages from both parents."""

    # Create empty vehicles matching p1's vehicle capacities
    child_vehicles = [Vehicle(v.max_capacity) for v in p1.vehicles]

    # Gather all packages from both parents
    merged_pkgs = []
    for v in p1.vehicles:
        merged_pkgs.extend(v.packages)
    for v in p2.vehicles:
        merged_pkgs.extend(v.packages)

    # Shuffle for randomness
    random.shuffle(merged_pkgs)

    # Track packages we've already added
    seen = set()

    for pkg in merged_pkgs:
        if pkg.uid in seen:
            continue
        seen.add(pkg.uid)

        # Try to place the package in the first vehicle where it fits
        for cv in child_vehicles:
            assign=False
            if cv.current_capacity + pkg.weight <= cv.max_capacity:
                cv.add_package(copy.deepcopy(pkg))
                assign=True
                break
        if assign==False:
            print("could not assign package!")
        # If it doesn't fit in any vehicle, we just drop it (skip it)

    return Solution(child_vehicles)


def pairs(solutions):
    random.shuffle(solutions)
    parent_pairs = []

    for i in range(0, len(solutions) - 1, 2):  # safer
        parent1 = solutions[i]
        parent2 = solutions[i + 1]
        parent_pairs.append((parent1, parent2))  

    return parent_pairs

def selection(population_size,solutions):
    prop=0
    prev_cum=0
    cum=0
    for solution in solutions:
    
        prop=solution. probability(population_size)
        cum=prop+prev_cum
        solution.set_cumulative(cum)
        prev_cum+=prop
    return solutions
def parents(solutions,pop_size):
    parent=[]
    i=0
    while i != pop_size:
        rand=random.random()
        for sol in solutions:
            if sol.cumulative>rand or sol.cumulative==rand:
                parent.append(sol)
                i=i+1
                break
    return parent        



            



def population(vehicles,packages,population_size):
    solutions = []
    print("population is being created!")
    for i in range(0,population_size):
        print(f"Solution number {i+1} is being created!")
       
        sol = generateSolution(vehicles,packages)
        if  sol==None:
             print("Could not find a solution!!")
             exit(1)
        else:
            solutions.append(sol)
            
           
    
    return solutions

def generateSolution(vehicles,packages):
    
    max_trys=50+3*len(packages)
    for i in range(0,(max_trys)):
        temp_vehicles = copy.deepcopy(vehicles)
        temp_packages = packages[:] 
        random.shuffle(temp_vehicles)
        random.shuffle(temp_packages)
        for package in temp_packages:
            x, y = package.destination
            assign=False
            for vehicle in temp_vehicles:
                if vehicle.current_capacity + package.weight <= vehicle.max_capacity:
                    vehicle.add_package(package)
                    assign=True
                    break
            if assign==False:
                break
        else:
                 return Solution(temp_vehicles)
        for idx, vehicle in enumerate(temp_vehicles, 1):
            distance = Solution.calculate_vehicle_distance(vehicle)
            print(f"\nVehicle {idx}:")
            print(f"  Max Capacity: {vehicle.max_capacity} kg")
            print(f"  Current Load: {vehicle.current_capacity} kg")
            print(f"  Route Distance: {distance:.2f} km")
            if not vehicle.packages:
                print("  Packages: (none)")
            else:
                print("  Packages:")
                for pkg in vehicle.packages:
                    x, y = pkg.destination
                    print(f"    - To ({x}, {y}), {pkg.weight}kg, Priority {pkg.priority}")
        
       
    return None
if __name__ == "__main__":
    main()