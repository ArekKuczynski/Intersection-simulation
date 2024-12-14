class SimData(object):
    '''Classic Singleton class containing global params'''
    _instance = None
    _cars = []
    _time_step = 1
    _areas = {1: False, 2: False, 3: False, 4: False}

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

    @property
    def areas(self):
        return self._areas

    @time_step.setter
    def areas(self, value):
        self._areas = value

    @staticmethod
    def reset_params() -> None:
        global_params = SimData()
        global_params._cars.clear()
