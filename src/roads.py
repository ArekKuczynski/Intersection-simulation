# --------------------|----|---------------------- < road_one
# --------------------|----|---------------------- < road_two
#                     |    |
#                     |    |
#                     |    |
#                     |    |
#                     ^    ^
#             road_three  road_four                 

class Roads():
    def __init__(self,characteristic_points = None):
        self.characteristic_points = characteristic_points

    # automatyczne obliczanie punktów charakterystycznych
    def get_characteristic_points(self):
        self.characteristic_points = [
            (295,250), # road_one x road_three
            (305,250), # road_one x road_four
            (295,240), # road_two x road_three
            (305,240), # road_two x road_four
            ]
        return self.characteristic_points
    
    def get_end_points(self, number: int):
        #### WAŻNE : Przy losowaniu ( lub tutaj ) inta, trzeba brać pod uwagę 
        #### to, że jeśli zaczyna z np. (0,240) to end_point nie może być równy (0,250)
        #### bo nie uwzględniamy przypadku, gdy zawraca
        
        if number == 1: 
            end_point = (300,250) # road_one
        elif number == 2:
            end_point = (600,240) # road_two
        elif number == 3:
            end_point = (295,0)   # road_three
        return end_point
    
    def get_start_points(self, number: int):
        if number == 1: 
            start_point = (600,250)  # road_one
        elif number == 2:
            start_point = (0,240)  # road_two
        elif number == 3:
            start_point = (305,0)  # road_three
        return start_point:

    def get_road(self,position,end_point): # sprawdza na której jest drodze na podstawie współrzędnej
        if position not in self.characteristic_points:    
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
        else:
            if end_point[1] == 250:
                return 1
            elif end_point[1] == 240:
                return 2
            elif end_point[0] == 305:
                return 4
            else:
                return "Error"
        
        ## Będzie trzeba też uwarunkować gdy np zaczyna w (600,250) i jedzie do (295,0)
        ## żeby dobiero na drugim punkcie charakterystycznym, który napotka zmienił kierunek
        ## można uwarunkować to, dając start_pointy do get_road albo ręcznie warunki na punktach charakterystycznych
        

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

