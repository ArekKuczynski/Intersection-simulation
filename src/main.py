import time
import random
import os
import math

from data import SimData
from car import Car
from roads import Roads


def build_cars(cars_num: int, velocity: int, length: int) -> None:
    """Build cars objects in the SimData cars list"""
    for num in range(cars_num):
        random.ra
        rand_road = random.randint(1,3)
        start_pos = roads.get_start_points(rand_road)

        # rand_road = random.randint(1,3)
        # end_point = roads.get_end_points()
        car = Car(f"C{num}",start_pos, velocity, length)
        sim_data.cars.append(car)

def simulation(time_step:int, debug = False, max_iter=math.inf) -> None:
    src_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(src_dir, "..", "logs.txt")
    log_file = open(log_file_path, "w")

    iter = 0
    while True:
        print(f"\n\n\n=== ITER:{iter} ===")
        curent_cars_pos = []
        for car in sim_data.cars:
            curent_cars_pos.append((car.x, car.y))
            car.start_engine()
            
            road = roads.get_road((car.x, car.y), None) # na razie None
            print(f"car_id:{car.id}, road: {road}") if debug else 0

            car.move(road)
            print(f"car_id:{car.id}, pos: (x={car.x}, y={car.y})") if debug else 0

        log_file.writelines(f"{iter}: {curent_cars_pos}\n")
        if iter == max_iter:
            break
        iter += 1
        time.sleep(time_step)
    
    log_file.close()

if __name__ == "__main__":
    print("Podaj wartości początkowe:")
    cars_num = int(input("Podaj liczbe aut w symulacji:"))
    velocity = int(input("Prędkość samochodu:"))
    length = int(input("Długość samochodu:"))

    sim_data = SimData()
    roads = Roads()

    build_cars(cars_num, velocity, length)

    # Symulacja:
    sim_data.time_step = 0.5
    simulation(sim_data.time_step, debug=True, max_iter=300)

