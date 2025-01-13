import subprocess
import pandas as pd
import ast

def load_parameters(file):
    
    with open(file, 'r') as file:
        data = file.read()

    parameters = ast.literal_eval(data)
    return parameters

def grid_search_simulation():
    
    parameters = load_parameters('parameters.txt')
    car_values = parameters.get("car_values", [])
    type_values = parameters.get("type_values", [])
    velocity_values = parameters.get("velocity_values", [])
    length_values = parameters.get("length_values", [])
    
    results = []
    
    for type in type_values:
        for car in car_values:
            for velocity in velocity_values:
                for length in length_values:
        
                    input_data = f"{type}\n{car}\n{velocity}\n{length}"
                    
                    proces = subprocess.run(
                        ['python','src/main.py'],
                        input = input_data,
                        capture_output = True,
                        text = True
                    )
                    
                    output_lines = proces.stdout.strip().splitlines() 
                    last_line = output_lines[-1:]  
                    iter = "\n".join(last_line)  
                    
                    result = {
                        "Type": type,
                        "Cars": car,
                        "Velocity": velocity,
                        "Length": length,
                        "Iter": iter
                    }
                    results.append(result)

    df = pd.DataFrame(results)
    df.to_csv("exploration_results.csv", index=False)

grid_search_simulation()