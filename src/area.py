class Area():
    # każdy samochód w kazdej iteracji żeby miał liczbę z get_area ( roads.py )
    # Wtedy tą liczbe wprowadzimy do obiektów Area, i one zmienią swój status 
    # na podstawie tego statusu zrobi się logikę na skrzyżowaniu 
    
    # get_area_list lista wartości zwróconych przez get_area dla każdego cara
    # a - liczba od 1 do 4, wskazuje, który to jest obszar na skrzyżowaniu (1-4)
    def __init__(self,a): 
        self.status = 0 
        self.a = a
    
    # zakłdam, że dwa samochody nie wjadą w tym samym momencie na obszar
    def check_status(self, get_area_list: list):  # ZMIANA NAZWY, bo traktowało self.status w return jako wywołanie funkcji
        if self.a in get_area_list:
            self.status = 1
            return self.status
        else:
            self.status = 0
            return self.status
    
    def get_status(self):
        return self.status
