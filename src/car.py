from data import SimData

class Car():
    """Class for making a car object"""
    def __init__(self, id: int, starting_position: tuple, velocity: float, length: float):
        self.sim_data = SimData()
        self.id = id
        self.x, self.y = starting_position
        self.velocity = velocity
        self.length = length
        self.started = False

    def start_engine(self):
        if not self.started:
            if len(self.sim_data.cars) == 1:
                self.started = True
            else:
                for car in self.sim_data.cars:
                    while car.id <= self.id:
                        if car.x != self.x: # zmienić na nierówność uzwzgędniającą długości samochodu i dopisać przypadek dla 1 samochodu
                            self.started = True
                        break

    def moving_forward(self, number: int) -> None:
        """Method for moving forward. Don't use in main.py"""
        if number == 1:
            self.x -= self.velocity * self.sim_data.time_step
        elif number == 2:
            self.x += self.velocity * self.sim_data.time_step
        elif number == 3:
            self.y -= self.velocity * self.sim_data.time_step
        else:
            self.y += self.velocity * self.sim_data.time_step

    def turning_right(self) -> None:
        """Method for turning right. Don't use in main.py"""
        pass

    def turning_left(self) -> None:
        """Method for turning left. Don't use in main.py"""
        pass

    def move(self, number_of_road: int) -> None:
        """Method used in main.py"""
        print(self.started)
        if self.started:
            self.moving_forward(number_of_road)
            # if number_of_road == 1:
            #     pass
            # elif number_of_road == 2:
            #     pass
            # elif number_of_road == 3:
            #     pass
            # else:
            #     pass
    
    def test(self):
        sim_data = SimData()
        sim_data.cars.append("xdCar")
        print(sim_data.cars)


    