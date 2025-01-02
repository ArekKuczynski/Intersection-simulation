import random
import math

from data import SimData

class Car():
    """Class for making a car object"""

    def __init__(self, id: int, starting_position: tuple, end_position: tuple, velocity: float, length: float):
        self.sim_data = SimData()
        self.id = id
        self.x, self.y = starting_position
        self.starting_position = starting_position
        self.end_position = end_position
        self.velocity = velocity
        self.length = length
        self.started = False

    def start_engine(self, road):
        """Function which checks if car is still moving or is starting moving"""
        if not self.started:
            if len(self.sim_data.cars) == 1:
                self.started = True
            elif (self.x, self.y) == self.starting_position:
                self.started = True
                for car in self.sim_data.cars:
                    if car.id > self.id:
                        continue
                    if car.id != self.id:  # przy znalezieniu 1 auta, które blokuje wjazd pętla jest przerywana
                        if road == 1:
                            if ((self.x - self.length - random.uniform(12, 24)) <= car.x and car.started) and car.y == self.y:
                                self.started = False
                                break
                        elif road == 2:
                            if ((self.x + self.length + random.uniform(12, 24)) >= car.x and car.started) and car.y == self.y:
                                self.started = False
                                break
                        elif road == 4:
                            if ((self.y + self.length + random.uniform(12, 24)) >= car.y and car.started) and car.x == self.x:
                                self.started = False
                                break

    def cars_trace(self):
        """Required distance to the car behind."""
        min_d = 3
        max_d = 7
        return random.randint(min_d, max_d) + (self.length / 2), min_d, max_d

    def distance_to_go(self, dimension: int, dim_values: str) -> float:
        """Calculate how much can car move relative to the car in front."""
        closest_car_in_front = None
        distance_to_car = math.inf

        if dimension not in (0, 1):
            raise "zły wymiar!"

        for car in self.sim_data.cars:
            if self.id == car.id:
                continue

            if dimension == 0:
                if self.y != car.y:
                    continue
                distance = car.x - self.x
            elif dimension == 1:
                if self.x != car.x:
                    continue
                distance = car.y - self.y

            if dim_values == "growing" and (distance > 0 and distance < distance_to_car):
                closest_car_in_front = car
                distance_to_car = distance
            elif dim_values == "decreases" and (-1 * distance > 0 and -1 * distance < distance_to_car):
                closest_car_in_front = car
                distance_to_car = -1 * distance

        if closest_car_in_front != None:
            trace, min_d, max_d = closest_car_in_front.cars_trace()
        else:
            trace = 0

        if ((distance_to_car - trace) > (self.velocity * self.sim_data.time_step + (self.length / 2))) or closest_car_in_front == None:
            random_offset = 0
            if int(self.velocity * self.sim_data.time_step) == self.velocity * self.sim_data.time_step:
                # potrzebne do lekkiej losowości
                random_offset = random.uniform(-0.3, 0.3)
            # wykonaj pełny ruch (nie ma auta w predykowanym ruchu).
            return round(self.velocity * self.sim_data.time_step + random_offset, 2)
        elif ((distance_to_car - self.length / 2) - (closest_car_in_front.length / 2 + max_d)) <= 0:
            return 0  # nie ruszaj się bo nie możesz (auto z przodu).
        else:
            # zbliż się do cara (jest z przodu, ale jesteś w stanie podjechać).
            return round(distance_to_car - (trace + self.length / 2), 2)

    def moving_forward(self, number: int, points: list) -> None:
        """Method for moving forward. Don't use in main.py"""
        if number == 1:
            if self.x <= self.end_position[0]:
                self.turning_off_engine()
                return None

            if (self.x - self.velocity * self.sim_data.time_step < points[0][0]) and (self.x > points[0][0]):
                self.x, self.y = points[0]
            elif (self.x - self.velocity * self.sim_data.time_step < points[1][0]) and (self.x > points[1][0]):
                self.x, self.y = points[1]
            elif (self.x + self.velocity * self.sim_data.time_step < points[1][0] + 5) and (self.x > points[1][0] + 5):
                self.x, self.y = points[1][0] + 5, points[1][1]
            else:
                self.x -= self.distance_to_go(0, "decreases")


        elif number == 2:
            if self.x >= self.end_position[0]:
                self.turning_off_engine()
                return None

            if (self.x + self.velocity * self.sim_data.time_step > points[3][0]) and (self.x < points[3][0]):
                self.x, self.y = points[3]
            elif (self.x + self.velocity * self.sim_data.time_step > points[2][0]) and (self.x < points[2][0]):
                self.x, self.y = points[2]
            elif (self.x + self.velocity * self.sim_data.time_step > points[2][0] - 5) and (self.x < points[2][0] - 5):
                self.x, self.y = points[2][0] - 5, points[2][1]
            else:
                self.x += self.distance_to_go(0, "growing")

        elif number == 3:
            if self.y <= self.end_position[1]:
                self.turning_off_engine()
                return None

            if (self.y - self.velocity * self.sim_data.time_step < points[2][1]) and (self.y > points[2][1]):
                self.x, self.y = points[2]
            else:
                self.y -= self.distance_to_go(1, "decreases")

        elif number == 4:  # brak możliwości wyłączenia silnika, ponieważ koniec jest na przecięciu dróg
            if (self.y + self.velocity * self.sim_data.time_step > points[1][1]) and (self.y < points[1][1]):
                self.x, self.y = points[1]
            elif (self.y + self.velocity * self.sim_data.time_step > points[3][1]) and (self.y < points[3][1]):
                self.x, self.y = points[3]
            elif (self.y + self.velocity * self.sim_data.time_step > points[3][1] - 5) and (self.y < points[3][1] - 5):
                self.x, self.y = points[3][0], points[3][1] - 5
            else:
                self.y += self.distance_to_go(1, "growing")

    def moving_at_roundabout(self, road: int, points: list) -> None:

        # Dojazd/po zjeździe z ronda
        if (self.x > points[5][0] or self.x < points[5][0]) and points[5][1] in [240, 250]:  # jest przed punktami 2,6 lub za 1,5
            points = [(290, 250), (310, 250), (290, 240), (310, 240)]
            self.move(road, points, 0)
            return None
        
        elif (road == 3 or road == 4) and points[5][1] < 235:  # jest przed punktem 4 lub za 3
            points = [None, (310, 250), (295, 235), (305, 235)]
            self.move(road, points, 0)
            return None
        
        # Ruch na rondzie
        
        
    def turning_off_engine(self) -> None:
        """Method for turning off the car's engine"""
        self.started = False


    def move(self, number_of_road: int, characteristic_points: list, road_type: int) -> None:
        """Method used only in main.py. If road_type = 0, intersection. If road_type = 1, roundabout"""
        if self.started:
            if road_type == 0:
                self.moving_forward(
                    number_of_road, characteristic_points)
            elif road_type == 1:
                self.moving_at_roundabout(number_of_road, characteristic_points)
