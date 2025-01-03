class SimData(object):
    '''Classic Singleton class containing global params for simulation model'''
    _instance = None
    _sim_mode = None
    _cars = []
    _time_step = 1

    def __new__(cls, sim_mode = None):
        if not cls._instance:
            if sim_mode != None:
                cls._sim_mode = sim_mode
            cls._instance = super(SimData, cls).__new__(cls)
        return cls._instance

    @property
    def sim_mode(self):
        return self._sim_mode

    @sim_mode.setter
    def sim_mode(self, value):
        self._sim_mode = value

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
