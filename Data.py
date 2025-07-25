from Aer_Qasm import CHSH
import GSPlotter as gsp
import numpy as np
import time

start = time.time()

def DataCollection():

	values = []
	shot_list = []
	iterator = 0
	for exponent in range(20,30):
		shots = 2**exponent
		for i in range(0,6):
			iterator += 1
			S = CHSH(shots)
			values.append(S)
			shot_list.append(shots)
			print(f"{iterator}: {S = }; {shots = }")
			print(f"S - 2√2: {S - 2.8284271247}")

	return values, shot_list


print("Starting calcuations...")

CHSH_Values, shots = DataCollection()

print("Manipulating data")

print(f"{CHSH_Values = }")
print(f"{shots = }")


NEW_CHSH_Values = [CHSH_Values, [2.8284271247]*60 ]
NEW_shots = [shots, shots]
print(f"{NEW_CHSH_Values = }")
print(f"{NEW_shots = }")

print(type(NEW_CHSH_Values[0]))

print(len(NEW_CHSH_Values[0]))
print(len(NEW_CHSH_Values[1]))

print(type(NEW_shots[0]))

print(len(NEW_shots[0]))
print(len(NEW_shots[1]))


print("Plotting...")

gsp.plotter(
    x_values=NEW_shots,             
    y_values=NEW_CHSH_Values,             
    xlabel='Shot Count', 
    ylabel='S Values',                   
    plot_labels=["Calculated S Values", "2√2"],                   
    title='Qasm Simulator Noise',                    
    filename='figure.png',                  
    colors=['red', 'black'],          
    line_styles=["--", "-"],          
)

end = time.time()
runtime = end - start
runtime_minutes = runtime/60

print(f"Program took {runtime_minutes} minutes")