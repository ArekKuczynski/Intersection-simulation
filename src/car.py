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
                            if ((self.x - self.length - 4) <= car.x and car.started) and car.y == self.y: # temp: 4
                                self.started = False
                                break
                        elif road == 2:
                            if ((self.x + self.length + 4) >= car.x and car.started) and car.y == self.y: # temp: 4
                                self.started = False
                                break
                        elif road == 4:
                            if ((self.y + self.length + 4) >= car.y and car.started) and car.x == self.x: # temp: 4
                                self.started = False
                                break

    def moving_forward(self, number: int, points: list, stop: bool) -> None:
        """Method for moving forward. Don't use in main.py"""
        if number == 1:
            if self.x <= self.end_position[0]:
                self.turning_off_engine()

            if stop:
                if (self.x - self.velocity * self.sim_data.time_step < points[0][0]) and (self.x, self.y != points[0]):
                    self.x, self.y = points[0]
                else:
                    self.x -= self.velocity * self.sim_data.time_step
            else:
                self.x -= self.velocity * self.sim_data.time_step

        elif number == 2:
            if self.x >= self.end_position[0]:
                self.turning_off_engine()

            if stop:
                if (self.x + self.velocity * self.sim_data.time_step > points[2][0]) and (self.x, self.y != points[2]):
                    self.x, self.y = points[2]
                else:
                    self.x += self.velocity * self.sim_data.time_step
            else:
                self.x += self.velocity * self.sim_data.time_step

        elif number == 3:
            self.y -= self.velocity * self.sim_data.time_step
            if self.y <= self.end_position[1]:
                self.turning_off_engine()

        else:  # brak możliwości wyłączenia silnika, ponieważ koniec jest na przecięciu dróg
            if stop:
                if (self.x, self.y) == points[3]:
                    self.y += self.velocity * self.sim_data.time_step
                else:
                    if self.y + self.velocity * self.sim_data.time_step > points[1][1]:
                        self.x, self.y = points[1]
                    else:
                        self.y += self.velocity * self.sim_data.time_step
            else:
                if (self.x, self.y) != points[1] and (self.x, self.y) != points[0]:
                    self.y += self.velocity * self.sim_data.time_step
                else:
                    self.x -= self.velocity * self.sim_data.time_step

    def turning_right(self) -> None:
        """Method for turning right. Don't use in main.py"""
        pass

    def turning_left(self) -> None:
        """Method for turning left. Don't use in main.py"""
        pass

    def turning_off_engine(self) -> None:
        """Method for turning off the car's engine"""
        #self.started = False

    def move(self, number_of_road: int, characteristic_points: list) -> None:
        """Method used only in main.py"""
        print(self.started)
        if self.started:
            # jeżeli musi skręcić z drogi 1 lub 2 na drogę 3
            if self.end_position[1] != self.y:
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

