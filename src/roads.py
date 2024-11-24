# --------------------|----|---------------------- < road_one
# --------------------|----|---------------------- < road_two
#                     |    |
#                     |    |
#                     |    |
#                     |    |
#                     ^    ^
#             road_three  road_four                 
#elo, get_road() niech zwraca inta od 1 do 4  <--- ok
# -----> jak coś to najpierw x potem y, ( oczywiste, ale lepiej się upewnić :v)


class Roads():
    def __init__(self,position = None,characteristic_points = None):
        self.position = position
        self.characteristic_points = characteristic_points

    # automatyczne obliczanie punktów charakterystycznych
    def get_characteristic_points(self):
        characteristic_points = [
            (295,250), # road_one x road_three
            (305,250), # road_one x road_four
            (295,240), # road_two x road_three
            (305,240), # road_two x road_four
            ]
        return characteristic_points
    
    def get_start_points(self, number: int):
        if number == 1: 
            start_point = (300,250) # road_one
        if number == 2:
            start_point = (0,240)  # road_two
        if number == 3:
            start_point = (305,0)  # road_four
        return start_point

    def get_road(self,position): # sprawdza na której jest drodze na podstawie współrzędnej
        if True:    #position not in self.characteristic_points:
            if position[1] == 250:
                return 1
            elif position[1] == 240:
                return 2
            elif position[0] == 295:
                return 3
            elif position[0] == 305:
                return 4
            else:
                return "Error"


    # obliczanie dalszych współrzędznych 


    def road_one():
        # y = 250   
        start_point = (300,250)
        return [start_point]

    def road_two():
        # y = 240
        start_point = (0,240)
        return

    def road_three(): 
        # x = 295
        return

    def road_four():
        # x = 305
        start_point = (305,0)
        return

