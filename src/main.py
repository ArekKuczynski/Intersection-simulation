import time
import random
import os
import math

from data import SimData
from car import Car
from preference import checking_preference
from roads import Roads
from area import Area


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
    areas = [Area(a) for a in range(1, 5)] # DODANA LISTA OBSZARÓW
    while len(sim_data.cars) != 0:
        print(f"\n\n\n=== ITER:{iter} ===")
        curent_cars_pos = []

        for car in sim_data.cars:
            if car.started == True:
                curent_cars_pos.append((round(car.x, 2), round(car.y, 2)))
            road = roads.get_road((car.x, car.y), car.end_position)
            print(f"\t-> car_id:{car.id}, road: {road}") if debug else 0

            car.start_engine(road)
            print(f"car_engine: {car.started}")

            area_list = [roads.get_area((c.x, c.y)) for c in sim_data.cars]
            for area in areas:
                area.check_status(area_list)

            current_area = roads.get_area((car.x, car.y))
            if checking_preference(car, areas, current_area):
                car.move(road, roads.characteristic_points)
            print(f"car_id:{car.id}, pos: (x={car.x}, y={car.y}), end_point: {car.end_position}") if debug else 0
            
            if car.started == False and (car.x, car.y) != car.starting_position:
                sim_data.cars.remove(car)
                del(car)

        print(f"area1: {areas[0].status}, area2: {areas[1].status}, area3: {areas[2].status}, area4: {areas[3].status}")
        log_file.writelines(f"{iter}: {curent_cars_pos}\n")
        if iter == max_iter:
            break
        iter += 1
        time.sleep(time_step)
    
    log_file.close()

if __name__ == "__main__":
    print("-- Podaj wartości początkowe: ---")
    cars_num = int(input("1. Podaj liczbe aut w symulacji: "))
    while True:
        velocity = int(input("2. Prędkość samochodu: "))
        if velocity > 9:
            print("Prędkość nie może przekraczać 9 metrów na sekundę!")
        elif velocity < 2:
            print("Długość nie może być mniejsza niż 2 metry na sekundę!")
        else:
            break
    
    while True:
        length = int(input("3. Długość samochodu: "))
        if length > 9:
            print("Długość nie może przekraczać 9 metrów!")
        elif length < 2:
            print("Długość nie może być mniejsza niż 2 metry!")
        else:
            break

    sim_data = SimData()
    roads = Roads()

    build_cars(cars_num, velocity, length)

    # Symulacja:
    sim_data.time_step = 0.5
    simulation(sim_data.time_step, debug=True)

