import math
# --------------------|----|---------------------- < road_one
# --------------------|----|---------------------- < road_two
#                     |    |
#                     |    |
#                     |    |
#                     |    |
#                     ^    ^
#             road_three  road_four                 


#                   Obszary
#                 ----1 2----
#                 ----3 4----
#                     | |
#                     | |


# Rondo
#
#                  _____
#               /        \
#--------------1|        C|6-------------
#--------------2|A        |5-------------
#               \ ____B_ / 
#                   3 4
#                   | |
#                   | |
# 1-6 to punkty charakterystyczne dla ronda ( tam gdzie rondo przecina się z drogą )

# Obszary na rondzie A, B, C ^^
class Roads():
    # Status 0 dla równorzędnego, 1 dla ronda
    def __init__(self, characteristic_points = None, status = 0):
        self.status = status
        self.characteristic_points = self.get_characteristic_points()

    # automatyczne obliczanie punktów charakterystycznych
    def get_characteristic_points(self):
        if self.status == 0:
            self.characteristic_points = [
                (295,250), # road_one x road_three
                (305,250), # road_one x road_four
                (295,240), # road_two x road_three
                (305,240), # road_two x road_four
                ]
        elif self.status == 1:
            self.characteristic_points = [
                # Punkty charakterystyczne koła, jak wyżej 
                #         vvvvvv
                (290,250), # 1
                (290,240), # 2
                (295,235), # 3
                (305,235), # 4
                (310,240), # 5
                (310,250)  # 6
            ]
        return self.characteristic_points
    
    def get_end_points(self, number: int,start_point):
        if start_point == (600,250): 
            end_point = [(0,250),(295,0)][number]
        elif start_point == (0,240):
            end_point = [(600,240),(295,0)][number]
        elif start_point == (305,0):
            end_point = [(0,250),(600,240)][number]
        return end_point
    
    def get_start_points(self, number: int):
        if number == 1: 
            start_point = (600,250)  # road_one
        elif number == 2:
            start_point = (0,240)  # road_two
        elif number == 3:
            start_point = (305,0)  # road_four
        return start_point
    
    def get_area(self, position: tuple) -> int:
        x = position[0]
        y = position[1]
        if self.status == 0:
            if (295 < x < 300) and (245 < y < 255):  
                return 1
            if ( 300 <= x < 310) and (245 <= y < 255): 
                return 2
            if (290 < x <= 300) and (240 <= y <= 245):  
                return 3
            if (300 < x < 305) and (235 < y < 245):  
                return 4
            else:
                return -1
        elif self.status == 1:
            offset = 6 # max 4.99? (wydłużanie obszaru na rondzie)
            offset_2 = 3
            if ( 287 < x < 290 + offset_2 ) and ( 240 < y < 245 + offset ): # 287 ~= 300 - sqrt(125) [zawyżone]
                return 1 # Obszar A
            elif ( 300 - offset < x < 305 ) and ( 233 < y < 235 + offset_2 ): # 233 ~= 245 - sqrt(125) [zawyżone]
                return 2 # Obszar B 
            elif ( 310 - offset_2 < x < 313 ) and ( 245 - offset < y < 250 ): # 313 ~= 300 + sqrt(125) [zawyżone]
                return 3 # Obszar C
            else:
                return -1
            

    def in_circle(self, position):
        r2 = (5 * math.sqrt(5))**2
        result = (position[0] - 300)**2 + (position[1] - 245)**2
        epsilon = 1
        return abs(result - r2) < epsilon

    def get_road(self, position: tuple, end_point: tuple): # sprawdza na której jest drodze na podstawie współrzędnej
        # w sumie można to ustandaryzować dając za endpointy zmienne
        if self.status == 0: # Równorzędne
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
                        return "Error" 
                if position == (295,250):
                    if end_point == (295,0):
                        return 3
                    elif end_point == (0,250):
                        return 1
                    else:
                        return "Error" 
                
                if position == (295,240):
                    if end_point == (600,240):
                        return 2
                    elif end_point == (295,0):
                        return 3
                    else:
                        return "Error" 
                    
                if position == (305,240):
                    if end_point == (600,240):
                        return 2
                    elif end_point == (0,250):
                        return 4
                    else:
                        return "Error" 
        
        if self.status == 1: # Rondo 
            if position not in self.characteristic_points:
                if position[1] == 250:
                    return 1
                elif position[1] == 240:
                    return 2
                elif position[0] == 295:
                    return 3
                elif position[0] == 305:
                    return 4
                elif self.in_circle(position):
                    return 5
                else:
                    return "Error"
            else:
                if position == (290,250) and end_point == (0,250): # Punkt charakterystyczny 1
                        return 1
                elif position == (295,235) and end_point == (295,0): # Punkt charakterystyczny 3
                        return 3
                elif position == (310,240) and end_point == (600,240): # Punkt charakterystyczny 5
                        return 2
                else:
                    return 5
