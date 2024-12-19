def checking_preference(current_car, areas: list, current_area: int): 
    """Function which decides if car can enter the intersection"""
    stop_points = [(310, 250), (290, 240), (305, 235)]
    if current_area == -1:  # Samochód nie jest przy skrzyżowaniu, może jechać dalej
        if (current_car.x, current_car.y) == stop_points[0]:
            if areas[1].get_status() == 0:
                return True
            else:
                return False
        elif (current_car.x, current_car.y) == stop_points[1]:
            if areas[2].get_status() == 0:
                return True
            else:
                return False
        elif (current_car.x, current_car.y) == stop_points[2]:
            if areas[3].get_status() == 0:
                return True
            else:
                return False
        else:
            return True
    
    # Jest na skrzyżowaniu, sprawdza czy kolejny obszr jest wolny
    if current_area == 1:
        if current_car.y == current_car.end_position[1]:  # nie skręca
            return True
        else:  # skręca w lewo z drogi 1 na 3
            if (areas[2].get_status() == 0) and (current_car.x == current_car.end_position[0]): 
                return True
            elif (current_car.x > current_car.end_position[0]):
                return True
            else:
                return False
            
    elif current_area == 2:
        if current_car.y == current_car.end_position[1]:  # nie skręca 
            if areas[0].get_status() == 0:
                return True
            else:
                return False
        else:  # zaraz skręci z drogi 4 na 2
            return True
        
    elif current_area == 3:
        if current_car.y == current_car.end_position[1]:  # nie skręca
            if areas[3].get_status() == 0:
                return True
            else:
                return False
        elif current_car.x == current_car.end_position[0]: # skręcił z drogi 1 na 3 i jedzie prosto
            return True
        else:  # skręca w prawo z drogi 2 na 3
            return True
    
    elif current_area == 4:
        if current_car.y == current_car.end_position[1]: # skręca w prawo z drogi 4 na 2 lub jedzie prosto z obszaru 3
            return True
        else:  # jedzie prosto lub skręca w lewo z drogi 4 na 1
            #if current_car.y > current_car.end_position[1] - 15:  # Chyba nie potrzebne
            if areas[1].get_status() == 0:
                return True
            else:
                return False



    