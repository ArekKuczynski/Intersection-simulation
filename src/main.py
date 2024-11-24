import time
import random
from data import SimData
from car import Car
from roads import Roads


def build_cars(cars_num: int, velocity: int, length: int) -> None:
    """Build cars objects in the SimData cars list"""
    for num in range(cars_num):
        rand_road = random.randint(1,3)

        start_pos = roads.get_start_points(2)
        car = Car(f"C{num}",start_pos, velocity, length)
        sim_data.cars.append(car)

def simulation(time_step:int, debug = False) -> None:
    iter = 0
    while True:
        print(f"\n\n\n=== ITER:{iter} ===")
        for car in sim_data.cars:
            car.start_engine()
            
            road = roads.get_road((car.x, car.y))
            print(f"car_id:{car.id}, road: {road}") if debug else 0

            car.move(road)
            print(f"car_id:{car.id}, pos: (x={car.x}, y={car.y})") if debug else 0

        # print("Cars:",sim_data.cars) if debug else 0


        iter += 1
        time.sleep(time_step)

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
    simulation(sim_data.time_step, debug=True)


