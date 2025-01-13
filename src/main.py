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

        car = Car(f"C{num}", start_pos, end_point, velocity, length)
        sim_data.cars.append(car)

def simulation(time_step:int, save_logs = True, debug = False, max_iter=math.inf) -> None:
    src_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(src_dir, "..", "logs.txt")
    log_file = open(log_file_path, "w")
    log_file.writelines(f"sim_mode: {sim_mode}\n")

    iter = 0
    if sim_mode == 0:  # DODANA LISTA OBSZARÓW
        areas = [Area(a) for a in range(1, 8)]
    else:
        areas = [Area(a) for a in range(1, 4)]
    last_current_cars_pos = None
    is_simulation_stalled = 0
    while len(sim_data.cars) != 0:
        print(f"\n\n\n=== ITER:{iter} ===")
        current_cars_pos = []

        for car in sim_data.cars:
            if car.started == True:
                current_cars_pos.append((round(car.x, 2), round(car.y, 2)))
            road = roads.get_road((car.x, car.y), car.end_position)
            print(f'\t[car_id: \"{car.id}\"]:') if debug else 0

            car.start_engine(road)
            print(f"- car_engine: {car.started}") if debug else 0

            area_list = [roads.get_area((c.x, c.y)) for c in sim_data.cars]
            for area in areas:
                area.check_status(area_list)

            current_area = roads.get_area((car.x, car.y))
            if checking_preference(car, areas, current_area, road, sim_mode):
                car.move(road, roads.characteristic_points)
            print(f"- pos: ({car.x}, {car.y}), end_point: {car.end_position}, current_road: {road}") if debug else 0
            
            if car.started == False and (car.x, car.y) != car.starting_position:
                sim_data.cars.remove(car)
                del(car)

        if debug and sim_mode == 0:
            print(f"\n[area1: {areas[0].status}, area2: {areas[1].status}, area3: {areas[2].status}, area4: {areas[3].status}]")
        elif debug and sim_mode == 1:
            print(f"\n[area A: {areas[0].status}, area B: {areas[1].status}, area C: {areas[2].status}]")
        if save_logs:
            log_file.writelines(f"{iter}: {current_cars_pos}\n")

        if iter == max_iter:
            break
        if current_cars_pos == last_current_cars_pos:
            is_simulation_stalled += 1
        else:
            is_simulation_stalled = 0
        if is_simulation_stalled > 9:
            raise Exception(f"Simulation stalled at {iter} iteration, after {is_simulation_stalled} iterations!")

        last_current_cars_pos = current_cars_pos
        iter += 1
        # time.sleep(time_step) # REAL TIME DISABLED/ENABLED?
    
    log_file.close()
    print("\n\n\n--- Wyniki: ---")
    print(f"Tryb symulacji: {sim_mode} \nIteracji: {iter} \nLiczba samochodód {cars_num}")
    print(f"Prędkość samochodów (m/s): {velocity} \nDługość samochodów (m): {length}")
    print(f"{iter}")

if __name__ == "__main__":
    print("--- Podaj wartości początkowe: ---")
    while True:
        sim_mode: int
        try:
            sim_mode = int(input("Wybierz tryb symulacji: \n  - '0': Skrzyżowanie równorzędne \n  - '1': Rondo\nSymulacja: "))
        except Exception as e:
            print("Niepoprawny tryb symulacji. Spróbuj ponownie.")
            continue
        if sim_mode not in [0, 1]:
            print("Niepoprawny tryb symulacji. Spróbuj ponownie.")
        else:
            break
    
    cars_num = int(input("1. Podaj liczbe aut w symulacji: "))
    while True:
        velocity = float(input("2. Prędkość samochodów (m/s): "))
        if velocity > 9: # więcej może powodować problemy
            print("Prędkość nie może przekraczać 9 metrów na sekundę!")
        elif velocity < 2:
            print("Długość nie może być mniejsza niż 2 metry na sekundę!")
        else:
            break
    while True:
        length = float(input("3. Długość samochodów (m): "))
        if length > 9:
            print("Długość nie może przekraczać 9 metrów!")
        elif length < 2:
            print("Długość nie może być mniejsza niż 2 metry!")
        else:
            break

    sim_data = SimData(sim_mode)
    roads = Roads(status = sim_mode)

    build_cars(cars_num, velocity, length)

    sim_data.time_step = 0.5 # in seconds
    simulation(sim_data.time_step, save_logs=True, debug=False)

