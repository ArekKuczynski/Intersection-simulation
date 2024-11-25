import matplotlib.pyplot as plt

def visualization(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    iterations = []
    for line in lines:
        iter_num, values = line.strip().split(': ')
        points = eval(values)
        iterations.append(points)

    plt.figure(figsize=(14, 8))  

    for i, points in enumerate(iterations):
       
        plt.cla() # czyszczenie po każdej iteracji
        plt.xlim(0, 600)
        plt.ylim(0, 400)
        plt.title(f'Wizualizacja symulacji - Iteracja {i + 1}')

        plt.axhline(y=250, color='red', linestyle='--', label='y = 250')  # Funkcja y = 250
        plt.axhline(y=240, color='blue', linestyle='--', label='y = 240')  # Funkcja y = 240
        plt.axvline(x=295, color='green', linestyle='--', label='x = 295')  # Funkcja x = 295
        plt.axvline(x=305, color='purple', linestyle='--', label='x = 305')  # Funkcja x = 305

        for x,y in points:
            plt.scatter(x, y, color='black') # rysowanie punktu
            
        
        
        # Wyświetlanie legendy
        plt.legend(loc='upper left')

        plt.pause(0.1) # pauza w sekundach po każdej iteracji

    plt.show()


visualization('logs.txt')
