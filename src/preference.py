def checking_preference(current_car, areas: list, current_area: int, road,  type: int):
    """Function which decides if car can enter the intersection"""
    if type == 0:
        return intersection_preference(current_car, areas, current_area)

    elif type == 1:
        return roundabout_preference(current_car, areas, current_area, road)


def intersection_preference(current_car, areas: list, current_area: int):
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
        # skręcił z drogi 1 na 3 i jedzie prosto
        elif current_car.x == current_car.end_position[0]:
            return True
        else:  # skręca w prawo z drogi 2 na 3
            return True

    elif current_area == 4:
        # skręca w prawo z drogi 4 na 2 lub jedzie prosto z obszaru 3
        if current_car.y == current_car.end_position[1]:
            return True
        else:  # jedzie prosto lub skręca w lewo z drogi 4 na 1
            # if current_car.y > current_car.end_position[1] - 15:  # Chyba nie potrzebne
            if areas[1].get_status() == 0:
                return True
            else:
                return False


def roundabout_preference(current_car, areas, current_area, road):
    stop_points = [(285, 240), (305, 230), (315, 250)]
    if current_area == -1:
        if (current_car.x, current_car.y) == stop_points[0]:  # A
            if areas[0].get_status() == 0:
                current_car.x, current_car.y = 289, 240
                return True
            else:
                return False
        elif (current_car.x, current_car.y) == stop_points[1]:  # B
            if areas[1].get_status() == 0:
                current_car.x, current_car.y = 305, 234
                return True
            else:
                return False
        elif (current_car.x, current_car.y) == stop_points[2]:  # C
            if areas[2].get_status() == 0:
                current_car.x, current_car.y = 309, 250
                return True
            else:
                return False
        else:
            return True
    else:  # Jest na rondzie w obszarze A, B lub C
        return True
    
    # elif current_area == 1:  # Jest na rondzie w obszarze A
    #     return True

    # elif current_area == 2:  # Jest na rondzie w obszarze B
    #     return True
    
    # elif current_area == 3:  # Jest na rondzie w obszarze C
    #     return True

