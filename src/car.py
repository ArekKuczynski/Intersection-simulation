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


    def calculate_new_point_on_circle(self, center: tuple, radius: float, start_point: tuple, distance: float) -> tuple:
        """
        Calculate new point at provided circle.
        The new point is the result of moving the original point counter-clockwise by the given distance.
        """
        x_c, y_c = center
        x_0, y_0 = start_point

        theta0 = math.atan2(y_0 - y_c, x_0 - x_c)
        delta_theta = distance / radius
        theta_new = theta0 + delta_theta

        x_new = x_c + radius * math.cos(theta_new)
        y_new = y_c + radius * math.sin(theta_new)

        return x_new, y_new


    def is_counterclockwise(self, center: tuple, start_point: tuple, test_point: tuple) -> bool:
        """
        Check if new point is in counter-clockwise direction.
        """
        x_c, y_c = center
        x_start, y_start = start_point
        x_test, y_test = test_point

        theta_start = math.atan2(y_start - y_c, x_start - x_c)
        theta_test = math.atan2(y_test - y_c, x_test - x_c)
        delta_theta = theta_test - theta_start

        result = delta_theta > 0
        return result


    def in_circle(self, position):
        r2 = (5 * math.sqrt(5))**2
        result = (position[0] - 300)**2 + (position[1] - 245)**2
        epsilon = 1
        return abs(result - r2) < epsilon


    def distance_to_go(self, dimension: int | str, dim_values: str) -> float | tuple:
        """
        Calculate how much can car move relative to the car in front.
        Possible dimensions: [0, 1, "circle"]
        Possible dimenstion values: 
        - for [0, 1] dimensions: ["growing", "decreases"],
        - for "circle" dimension: "counter-clock"
        """
        closest_car_in_front = None
        distance_to_car = math.inf

        center = (300, 245) # stały środek koła
        radius = math.sqrt(125)

        if dimension not in (0, 1, "circle"):
            raise Exception("zły wymiar!")

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
            elif dimension == "circle":
                if not self.in_circle((car.x, car.y)):
                    continue
                distance = math.sqrt((car.y - self.y)**2 + (car.x - self.x)**2) - 1 # -1 bo tak nie wiem dziwny blad
            else:
                distance = math.inf

            if dimension in (0, 1):
                if dim_values == "growing" and (distance > 0 and distance < distance_to_car):
                    closest_car_in_front = car
                    distance_to_car = distance
                elif dim_values == "decreases" and (-1 * distance > 0 and -1 * distance < distance_to_car):
                    closest_car_in_front = car
                    distance_to_car = -1 * distance
            elif dimension == "circle":
                result = self.is_counterclockwise(center, (self.x, self.y), (car.x, car.y))
                if dim_values == "counter-clock" and (result and distance < distance_to_car):
                    closest_car_in_front = car
                    distance_to_car = distance

        if closest_car_in_front != None:
            trace, min_d, max_d = closest_car_in_front.cars_trace()
        else:
            trace = 0


        # wykonaj pełny ruch (nie ma auta w predykowanym ruchu):
        if ((distance_to_car - trace) > (self.velocity * self.sim_data.time_step + (self.length / 2))) or closest_car_in_front == None:
            random_offset = 0
            if int(self.velocity * self.sim_data.time_step) == self.velocity * self.sim_data.time_step:
                random_offset = random.uniform(-0.3, 0.3)
            
            distance_to_go = self.velocity * self.sim_data.time_step + random_offset
            if dimension in (0, 1):
                return round(distance_to_go, 2)
            elif dimension == "circle":
                new_x, new_y = self.calculate_new_point_on_circle(center, radius, (self.x, self.y), distance_to_go)
                return round(new_x - self.x, 2), round(new_y - self.y, 2)
        # nie ruszaj się bo nie możesz (auto z przodu):
        elif ((distance_to_car - self.length / 2) - (closest_car_in_front.length / 2 + max_d)) <= 0:
            distance_to_go = 0
            if dimension in (0, 1):
                return distance_to_go
            elif dimension == "circle":
                return distance_to_go, distance_to_go
        # zbliż się do cara (jest z przodu, ale jesteś w stanie podjechać):
        else:
            distance_to_go = distance_to_car - (trace + self.length / 2)
            if dimension in (0, 1):
                return round(distance_to_go, 2)
            elif dimension == "circle":
                new_x, new_y = self.calculate_new_point_on_circle(center, radius, (self.x, self.y), distance_to_go)
                return round(new_x - self.x, 2), round(new_y - self.y, 2)


    def moving_forward(self, road: int, points: list) -> None:
        """Method for moving forward in intersection simulation mode. Don't use in main.py"""
        if road == 1:
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

        elif road == 2:
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

        elif road == 3:
            if self.y <= self.end_position[1]:
                self.turning_off_engine()
                return None

            if (self.y - self.velocity * self.sim_data.time_step < points[2][1]) and (self.y > points[2][1]):
                self.x, self.y = points[2]
            else:
                self.y -= self.distance_to_go(1, "decreases")

        elif road == 4:  # brak możliwości wyłączenia silnika, ponieważ koniec jest na przecięciu dróg
            if (self.y + self.velocity * self.sim_data.time_step > points[1][1]) and (self.y < points[1][1]):
                self.x, self.y = points[1]
            elif (self.y + self.velocity * self.sim_data.time_step > points[3][1]) and (self.y < points[3][1]):
                self.x, self.y = points[3]
            elif (self.y + self.velocity * self.sim_data.time_step > points[3][1] - 5) and (self.y < points[3][1] - 5):
                self.x, self.y = points[3][0], points[3][1] - 5
            else:
                self.y += self.distance_to_go(1, "growing")


    def moving_at_roundabout(self, road: int, points: list) -> None:
        """Method for moving forward in roundabout simulation mode. Don't use in main.py"""
        # Dojazd/po zjeździe z ronda
        # if (self.x > points[5][0] or self.x < points[0][0]) and points[5][1] in [240, 250]:  # jest przed punktami 2,6 lub za 1,5
        #     points = [(290, 250), (310, 250), (290, 240), (310, 240)]
        #     self.move(road, points, 0)
        #     return None
        
        # elif (road == 3 or road == 4) and points[5][1] < 235:  # jest przed punktem 4 lub za 3
        #     points = [None, (310, 250), (295, 235), (305, 235)]
        #     self.move(road, points, 0)
        #     return None
        
        if road == 1:
            if self.x <= self.end_position[0]:
                self.turning_off_engine()
                return None

            if (self.x - self.velocity * self.sim_data.time_step < points[5][0]) and (self.x > points[5][0]):
                self.x, self.y = points[5]
            elif (self.x + self.velocity * self.sim_data.time_step < points[5][0] + 5) and (self.x > points[5][0] + 5):
                self.x, self.y = points[5][0] + 5, points[5][1]
            else:
                self.x -= self.distance_to_go(0, "decreases")

        elif road == 2:
            if self.x >= self.end_position[0]:
                self.turning_off_engine()
                return None

            if (self.x + self.velocity * self.sim_data.time_step > points[1][0]) and (self.x < points[1][0]):
                self.x, self.y = points[1]
            elif (self.x + self.velocity * self.sim_data.time_step > points[1][0] - 5) and (self.x < points[1][0] - 5):
                self.x, self.y = points[1][0] - 5, points[1][1]
            else:
                self.x += self.distance_to_go(0, "growing")

        elif road == 3:
            if self.y <= self.end_position[1]:
                self.turning_off_engine()
                return None

            if (self.y - self.velocity * self.sim_data.time_step < points[2][1]) and (self.y > points[2][1]):
                self.x, self.y = points[2]
            else:
                self.y -= self.distance_to_go(1, "decreases")

        elif road == 4:
            if (self.y + self.velocity * self.sim_data.time_step > points[3][1]) and (self.y < points[3][1]):
                self.x, self.y = points[3]
            elif (self.y + self.velocity * self.sim_data.time_step > points[3][1] - 5) and (self.y < points[3][1] - 5):
                self.x, self.y = points[3][0], points[3][1] - 5
            else:
                self.y += self.distance_to_go(1, "growing")

        elif road == 5:
            distance_x, distance_y = self.distance_to_go("circle", "counter-clock")
            if ((self.y + distance_y < points[0][1]) and (self.y > points[0][1])) and \
            ((self.x + distance_x < points[0][0]) and (self.x > points[0][0])):
                self.x, self.y = points[0]
            elif ((self.y + distance_y < points[2][1]) and (self.y > points[2][1])) and \
            ((self.x + distance_x > points[2][0]) and (self.x < points[2][0])):
                self.x, self.y = points[2]
            elif ((self.y + distance_y > points[4][1]) and (self.y < points[4][1])) and \
            ((self.x + distance_x > points[4][0]) and (self.x < points[4][0])):
                self.x, self.y = points[4]
            else:
                self.x += distance_x
                self.y += distance_y


    def turning_off_engine(self) -> None:
        """Method for turning off the car's engine"""
        self.started = False


    def move(self, number_of_road: int, characteristic_points: list) -> None:
        """Method used only in main.py. If road_type = 0, intersection. If road_type = 1, roundabout"""
        if self.started:
            if self.sim_data.sim_mode == 0:
                self.moving_forward(number_of_road, characteristic_points)
            elif self.sim_data.sim_mode == 1:
                self.moving_at_roundabout(number_of_road, characteristic_points)
