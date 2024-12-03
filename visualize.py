import matplotlib.pyplot as plt

def visualization(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    iterations = []
    for line in lines:
        iter_num, values = line.strip().split(': ')
        points = eval(values)
        iterations.append(points)

    fig, ax = plt.subplots(figsize=(14, 8))  

    ax.set_xlim(0, 600)
    ax.set_ylim(0, 400)

    for i, points in enumerate(iterations):
        ax.cla()  # Czyszczenie bieżącej osi

        ax.set_xlim(0, 600)
        ax.set_ylim(0, 400)
        ax.set_title(f'Wizualizacja symulacji - Iteracja {i + 1}')

        ax.axhline(y=250, color='red', linestyle='--', label='y = 250')
        ax.axhline(y=240, color='blue', linestyle='--', label='y = 240')
        ax.axvline(x=295, color='green', linestyle='--', label='x = 295')
        ax.axvline(x=305, color='purple', linestyle='--', label='x = 305')

        for x, y in points:
            ax.scatter(x, y, color='black')

        ax.legend(loc='upper left')

        plt.pause(0.0000001) # nie da się krócej ( do sprawdzenia )

    plt.show()

visualization('logs.txt')
