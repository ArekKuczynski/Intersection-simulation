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
        possible_roads = [1, 2, 3]
        endpoints = [0,1]

        rand_road = random.choice(possible_roads)
        rand_endpoints = random.choice(endpoints)

        start_pos = roads.get_start_points(rand_road)
        end_point = roads.get_end_points(rand_endpoints,start_pos)

        car = Car(f"C{num}",start_pos, end_point, velocity, length)
        sim_data.cars.append(car)

def simulation(time_step:int, debug = False, max_iter=math.inf) -> None:
    src_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(src_dir, "..", "logs.txt")
    log_file = open(log_file_path, "w")

    iter = 0
    while len(sim_data.cars) != 0:
        print(f"\n\n\n=== ITER:{iter} ===")
        curent_cars_pos = []

        for car in sim_data.cars:
            curent_cars_pos.append((car.x, car.y))
            road = roads.get_road((car.x, car.y), car.end_position)
            print(f"car_id:{car.id}, road: {road}") if debug else 0

            car.start_engine(road)
            print(f"car_engine: {car.started}")

            car.move(road, roads.characteristic_points)
            print(f"car_id:{car.id}, pos: (x={car.x}, y={car.y}), end_point: {car.end_position}") if debug else 0

        log_file.writelines(f"{iter}: {curent_cars_pos}\n")
        if iter == max_iter:
            break
        iter += 1
        time.sleep(time_step)
    
    log_file.close()

if __name__ == "__main__":
    print("-- Podaj wartości początkowe: ---")
    cars_num = int(input("1. Podaj liczbe aut w symulacji: "))
    velocity = int(input("2. Prędkość samochodu: "))
    length = int(input("3. Długość samochodu: "))

    sim_data = SimData()
    roads = Roads()

    build_cars(cars_num, velocity, length)

    # Symulacja:
    sim_data.time_step = 0.5
    simulation(sim_data.time_step, debug=True, max_iter=300)

