class SimData(object):
    '''Classic Singleton class containing global params'''
    _instance = None
    _cars = []
    _time_step = 1

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(SimData, cls).__new__(cls)
        return cls._instance

    @property
    def cars(self):
        return self._cars

    @cars.setter
    def cars(self, value):
        self._cars = value

    @property
    def time_step(self):
        return self._time_step

    @time_step.setter
    def time_step(self, value):
        self._time_step = value

    @staticmethod
    def reset_params() -> None:
        global_params = SimData()
        global_params._cars.clear()
