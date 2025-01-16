import os
import subprocess

# Parameters for the input file
base_input = {
    "N": 20,
    "grid_size": 10,
    "iterations": 15000,
    "temperature(K)": 0,  # This will be updated for each simulation
    "potential": "inverse",
    "initial_coordinates": "random",
}

# Directories for inputs and outputs
input_dir = os.path.abspath("inputs")
output_dir = os.path.abspath("outputs")
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# Range of temperatures (0 to 4 inclusive, with 20 steps)
temperatures = [round(t, 2) for t in [i * 4 / 19 for i in range(20)]]

# Run simulations
for i, temp in enumerate(temperatures):
    # Update temperature in the base input
    base_input["temperature(K)"] = temp

    # Create input file
    input_filename = os.path.join(input_dir, f"input_{i}.txt")
    with open(input_filename, "w") as file:
        for key, value in base_input.items():
            file.write(f"{key}: {value}\n")

    # Define output file
    output_filename = os.path.join(output_dir, f"output_{i}.txt")

    # Run simulation and save output
    print(f"Running simulation {i + 1} for temperature {temp} K...")
    with open(output_filename, "w") as outfile:
        subprocess.run(["py", "meltdown.py", input_filename], stdout=outfile, stderr=subprocess.STDOUT)

print("All simulations completed. Outputs saved to the 'outputs' directory.")
