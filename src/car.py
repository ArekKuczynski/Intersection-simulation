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
            elif dim_values == "decreases"and (-1 * distance > 0 and -1 * distance < distance_to_car):
                closest_car_in_front = car
                distance_to_car = -1 * distance

        if closest_car_in_front != None:
            trace, min_d, max_d = closest_car_in_front.cars_trace()
        else:
            trace = 0

        if ((distance_to_car - trace) > (self.velocity * self.sim_data.time_step + (self.length / 2))) or closest_car_in_front == None:
            random_offset = 0
            if int(self.velocity * self.sim_data.time_step) == self.velocity * self.sim_data.time_step:
                random_offset = random.uniform(-0.3, 0.3) # potrzebne do lekkiej losowości
            return round(self.velocity * self.sim_data.time_step + random_offset, 2) # wykonaj pełny ruch (nie ma auta w predykowanym ruchu).
        elif ((distance_to_car - self.length / 2) - (closest_car_in_front.length / 2 + max_d)) <= 0:
            return 0 # nie ruszaj się bo nie możesz (auto z przodu).
        else:
            return round(distance_to_car - (trace + self.length / 2), 2) # zbliż się do cara (jest z przodu, ale jesteś w stanie podjechać).

    def moving_forward(self, number: int, points: list, stop: bool) -> None:
        """Method for moving forward. Don't use in main.py"""
        if number == 1:
            if self.x <= self.end_position[0]:
                self.turning_off_engine()
                return None

            if stop:
                if (self.x - self.velocity * self.sim_data.time_step < points[0][0]) and (self.x > points[0][0]):
                    self.x, self.y = points[0]
                elif (self.x - self.velocity * self.sim_data.time_step < points[1][0]) and (self.x > points[1][0]):
                    self.x, self.y = points[1]
                elif (self.x + self.velocity * self.sim_data.time_step < points[1][0] + 5) and (self.x > points[1][0] + 5):
                    self.x, self.y = points[1][0] + 5, points[1][1]
                else:
                    self.x -= self.distance_to_go(0, "decreases")

            else:
                self.x -= self.velocity * self.sim_data.time_step

        elif number == 2:
            if self.x >= self.end_position[0]:
                self.turning_off_engine()
                return None

            if stop:
                if (self.x + self.velocity * self.sim_data.time_step > points[3][0]) and (self.x < points[3][0]):
                    self.x, self.y = points[3]
                elif (self.x + self.velocity * self.sim_data.time_step > points[2][0]) and (self.x < points[2][0]):
                    self.x, self.y = points[2]
                elif (self.x + self.velocity * self.sim_data.time_step > points[2][0] - 5) and (self.x < points[2][0] - 5):
                    self.x, self.y = points[2][0] - 5, points[2][1]
                else:
                    self.x += self.distance_to_go(0, "growing")

            else:
                self.x += self.velocity * self.sim_data.time_step

        elif number == 3:
            if self.y <= self.end_position[1]:
                self.turning_off_engine()
                return None

            if (self.y - self.velocity * self.sim_data.time_step < points[2][1]) and (self.y > points[2][1]):
                self.x, self.y = points[2]
            else:
                self.y -= self.distance_to_go(1, "decreases")

        elif number == 4:  # brak możliwości wyłączenia silnika, ponieważ koniec jest na przecięciu dróg
            if stop:
                if (self.y + self.velocity * self.sim_data.time_step > points[1][1]) and (self.y < points[1][1]):
                    self.x, self.y = points[1]
                elif (self.y + self.velocity * self.sim_data.time_step > points[3][1]) and (self.y < points[3][1]):
                    self.x, self.y = points[3]
                elif (self.y + self.velocity * self.sim_data.time_step > points[3][1] - 5) and (self.y < points[3][1] - 5):
                    self.x, self.y = points[3][0], points[3][1] - 5
                else:
                    self.y += self.distance_to_go(1, "growing")

            else:
                if (self.x, self.y) != points[1] and (self.x, self.y) != points[0]:
                    self.y += self.velocity * self.sim_data.time_step
                else:
                    self.x -= self.velocity * self.sim_data.time_step

    def turning_off_engine(self) -> None:
        """Method for turning off the car's engine"""
        self.started = False

    def move(self, number_of_road: int, characteristic_points: list) -> None:
        """Method used only in main.py"""
        if self.started:
            # jeżeli musi skręcić z drogi 1 lub 2 na drogę 3
            if True:
                self.moving_forward(
                    number_of_road, characteristic_points, True)
                # if (self.x, self.y) == characteristic_points[0]:
                #     self.turning_left()
                # elif (self.x, self.y) == characteristic_points[2]:
                #     self.turning_right()

            # jeżeli musi skręcić z drogi 4 na drogę 1 lub 2
            # elif self.end_position[0] != self.x:
            #     self.moving_forward(
            #         number_of_road, characteristic_points, True)
            #     if (self.x, self.y) == characteristic_points[1]:
            #         self.turning_left()
            #     elif (self.x, self.y) == characteristic_points[3] and self.end_position[0] == self.x:
            #         self.turning_right()

            else:
                self.moving_forward(
                    number_of_road, characteristic_points, False)

