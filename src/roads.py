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
        self.characteristic_points = self.get_characteristic_points()

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
        # dodać block na endpointy dla określonych start pointów ^^ 
        # aby pozbyć się poziomu ifów można endpointy dać do listy i usuwac jeden w zaelżności od startpointa 
        if number == 1: 
            end_point = (0,250)   # road_one
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
            start_point = (305,0)  # road_four
        return start_point

    def get_road(self,position,end_point): # sprawdza na której jest drodze na podstawie współrzędnej
        # w sumie można to ustandaryzować dając za endpointy zmienne
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
            if position == (305,250):
                if end_point == (0,250):
                    return 1
                elif end_point == (295,0):
                   return 1
                else:
                    return "Nie powinno być tego end pointa, coś w warunkach blocka get_end_points jest źle" # wersja robocza 
            if position == (295,250):
                if end_point == (600,240):
                    return 3
                elif end_point == (0,250):
                    return 1
                else:
                    return "Nie powinno być tego end pointa, coś w warunkach blocka get_end_points jest źle" # wersja robocza 
            
            if position == (295,240):
                if end_point == (600,240):
                    return 2
                elif end_point == (295,0):
                    return 3
                else:
                    return "Nie powinno być tego end pointa, coś w warunkach blocka get_end_points jest źle" # wersja robocza 
                 
            if position == (305,240):
                if end_point == (600,240):
                    return 2
                elif end_point == (0,250):
                    return 4
                else:
                    return "Nie powinno być tego end pointa, coś w warunkach blocka get_end_points jest źle" # wersja robocza     

    # obliczanie dalszych współrzędznych 
    # jeszcze nwm, może być to wcale nie potrzebne 
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

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

