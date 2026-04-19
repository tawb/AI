import re
import sys
import math
import json

class Vehicle:
    def __init__(self, max_capacity):
        self.max_capacity = max_capacity  # max weight capacity
        self.current_capacity = 0         # current weight
        self.packages = []
        self.rank=0
    def __hash__(self):
       return hash(self.uid)

    def __eq__(self, other):
       return isinstance(other, Package) and self.uid == other.uid
    def add_package(self, package):
        if self.current_capacity + package.weight <= self.max_capacity:
            self.packages.append(package)
            self.current_capacity += package.weight
            print("Package added.")
        else:
            print("Cannot add package. Exceeds vehicle capacity.")
class Package:
    def __init__(self, x, y, weight, priority,uid):
        self.uid = uid 
        self.destination = (x, y)
        self.weight = weight
        self.priority = priority
class Solution:
    def __init__(self, vehicles):
        self.vehicles = vehicles  # list of Vehicle objects
        self.total_distance = 0
        self.fit=0
        self.prop=0
        self.cumulative=0
    def euclidean_distance(p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    @staticmethod
    def calculate_vehicle_distance(vehicle):
        if not vehicle.packages:
            return 0

        total_distance = 0
        current_location = (0, 0)

        for package in vehicle.packages:
            next_location = package.destination
            total_distance += Solution.euclidean_distance(current_location, next_location)
            current_location = next_location

        return total_distance

    def calculate_distance(self):
        self.total_distance = 0  # Reset in case it's called again
        for vehicle in self.vehicles:
            dist = self.calculate_vehicle_distance(vehicle)
            self.total_distance += dist
        return self.total_distance
    def fitness(self):
        self.fit=1/self.calculate_distance()
        return self.fit
    def set_rank(self,rank):
        self.rank=rank
        return self.rank
    def probability(self,population_size):
        self.prop=(2*(population_size-self.rank+1))/(population_size*(population_size+1))
        return self.prop
    def set_cumulative(self,cumulative):
        self.cumulative=cumulative
        return self.cumulative

def load_data_json(path):
    """
    Read packages and vehicle info from a JSON file.

    Expected structure:
    {
      "packages": {
        "pkg1": { "location": [10, 10], "weight_kg": 10, "priority": 1 },
        ...
      },
      "vehicles": {
        "vanA": { "capacity_kg": 50 },
        ...
      }
    }
    """
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: file not found → {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: JSON parsing failed → {e}", file=sys.stderr)
        sys.exit(1)

    packages = {}
    for name, info in data.get("packages", {}).items():
        try:
            x, y = info["location"]
            packages[name] = {

                "location": (int(x), int(y)),
                "weight": int(info["weight_kg"]),
                "priority": int(info["priority"]),
            }
        except (KeyError, ValueError) as e:
            print(f"Warning: skipping malformed package '{name}' → {e}", file=sys.stderr)

    vehicles = {}
    for name, info in data.get("vehicles", {}).items():
        try:
            vehicles[name] = {"capacity": int(info["capacity_kg"])}
        except (KeyError, ValueError) as e:
            print(f"Warning: skipping malformed vehicle '{name}' → {e}", file=sys.stderr)

    return packages, vehicles


def build_objects(packages_dict, vehicles_dict):
    vehicle_objs = [Vehicle(v["capacity"]) for v in vehicles_dict.values()]

    package_objs = [
        Package(
            x        = info["location"][0],
            y        = info["location"][1],
            weight   = info["weight"],
            priority = info["priority"],
            uid      = name                     # ← NEW
        )
        for name, info in packages_dict.items() # ← iterate with key
    ]
    return vehicle_objs, package_objs



def read_data(path):
    pkgs, vehs = load_data_json(path)

    # Console summary
    print("Packages:")
    if not pkgs:
        print("  (none found)")
    for k, info in pkgs.items():
        print(
            f"  {k}: location={info['location']}, weight={info['weight']}kg, priority={info['priority']}"
        )

    print("\nVehicles:")
    if not vehs:
        print("  (none found)")
    for k, info in vehs.items():
        print(f"  {k}: capacity={info['capacity']}kg")

    print(f"\nNumber of vehicles: {len(vehs)}")

    return build_objects(pkgs, vehs)


# ---------- Main ----------

if __name__ == "__main__":
    # Pass a custom path with `python logistics_routing_json.py myfile.json`
    data_file = sys.argv[1] if len(sys.argv) > 1 else "data.json"

    vehicle_objs, package_objs = read_data(data_file)

    # Simple first‑fit assignment
    for pkg in package_objs:
        for vehicle in vehicle_objs:
            if vehicle.current_capacity + pkg.weight <= vehicle.max_capacity:
                vehicle.add_package(pkg)
                break
        else:
            print(f"Package {pkg.destination} could not be assigned to any vehicle.")

    solution = Solution(vehicle_objs)
    total_dist = solution.calculate_distance()

    print("\nVehicle Assignments:")
    for idx, v in enumerate(vehicle_objs, 1):
        dist = Solution.calculate_vehicle_distance(v)
        print(f"\nVehicle {idx}:")
        print(f"  Max Capacity: {v.max_capacity} kg")
        print(f"  Current Load: {v.current_capacity} kg")
        print(f"  Route Distance: {dist:.2f} km")
        if not v.packages:
            print("  Packages: (none)")
        else:
            for pkg in v.packages:
                x, y = pkg.destination
                print(f"    - To ({x}, {y}), {pkg.weight}kg, Priority {pkg.priority}")

    print(f"\nTotal distance across all vehicle routes: {total_dist:.2f} km")

