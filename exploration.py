import subprocess
import pandas as pd
import ast
import time

def load_parameters(file):
    
    with open(file, 'r') as file:
        data = file.read()

    parameters = ast.literal_eval(data)
    return parameters

def grid_search_simulation():
    st = time.time()
    
    parameters = load_parameters('parameters.txt')
    car_values = parameters.get("car_values", [])
    type_values = parameters.get("type_values", [])
    velocity_values = parameters.get("velocity_values", [])
    length_values = parameters.get("length_values", [])
    
    results = []
    n=0
    repetitions = 5 # min. 3 
    for type in type_values:
        for car in car_values:
            for velocity in velocity_values:
                for length in length_values:
                    for i in range(repetitions):
                        n += 1
                        pt = time.time()
                        error = 0
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
                        
                        if  iter[0:8] == '=== ITER':
                            error = 1
                            #raise Exception(f"Simulation stalled at {iter} iteration, after {10} iterations!")
                        
                        print(f"================================== Parametry próby {n} ==================================")
                        
                        if error == 0:
                            try:
                                result = {
                                    "Type": type,
                                    "Cars": car,
                                    "Velocity": velocity,
                                    "Length": length,
                                    "Iter": iter,
                                    "Efficiency": round(int(car)/int(iter),2)
                                }
                            except:
                                result = {
                                    "Type": type,
                                    "Cars": car,
                                    "Velocity": velocity,
                                    "Length": length,
                                    "Iter": "None",
                                    "Efficiency": "None"
                                }
                            results.append(result)
                        else:
                            print(f"Simulation stalled at {iter} iteration, after {10} iterations!")
                            result = {
                                "Type": type,
                                "Cars": car,
                                "Velocity": velocity,
                                "Length": length,
                                "Iter": None,
                                "Efficiency": None
                            }
                            results.append(result)
                        
                        print(f"Czas od rozpoczęcia całkowitego: {round(time.time() - st,2)} ")
                        print(f"Czas wykonania próby: {round(time.time() - pt,2)} ")
                        print(f"i = {i}")
                        print(f"type = {type}")
                        print(f"car = {car}")
                        print(f"velocity = {velocity}")
                        print(f"length = {length}")
                        print("")

    df = pd.DataFrame(results)
    df.to_csv("exploration_results.csv", index=False)
    print(f"Czas wykonywania się symulacji całkowitej: {round(time.time() - st,2)}")

grid_search_simulation()
