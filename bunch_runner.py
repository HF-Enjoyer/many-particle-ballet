import os
import subprocess
import time

# Path to the input file
input_file = "input.txt"

# Path to the consolidated output file
output_file = "simulation_results_polymer_inverse.csv"

# Base parameters for the input file
base_input = {
    "N": 20,
    "grid_size": 10,
    "iterations": 8000,
    "temperature(K)": 0,  # This will be updated for each simulation
    "potential": "inverse",
    "polymer": "True",
    "initial_coordinates": "random",
}

# Adjustable temperature range and step size
temperature_min = 0  # Minimum temperature
temperature_max = 4  # Maximum temperature
temperature_step = 0.3  # Step size for temperature

# Generate the range of temperatures
temperatures = [round(t, 2) for t in 
                [temperature_min + i * temperature_step for i in range(int((temperature_max - temperature_min) / temperature_step) + 1)]]

# Initialize the output file with headers
with open(output_file, "w") as outfile:
    outfile.write("T,d,F\n")  # CSV header
t0 = time.time()
# Run simulations
for i, temp in enumerate(temperatures):
    # Update temperature in the base input
    base_input["temperature(K)"] = temp

    # Overwrite the input file with updated parameters
    with open(input_file, "w") as file:
        for key, value in base_input.items():
            if key == "initial_coordinates":
                file.write(f"{key}:\n{value}\n")  # Place "random" on the next line
            else:
                file.write(f"{key}: {value}\n")

    # Capture simulation output
    print(f"Running simulation {i + 1} for temperature {temp} K...")
    process = subprocess.run(
        ["py", "meltdown.py", input_file],
        capture_output=True,
        text=True,
    )
    
    # Parse the simulation output
    output_lines = process.stdout.splitlines()
    line1 = output_lines[0] if len(output_lines) > 0 else "N/A"
    line2 = output_lines[1] if len(output_lines) > 1 else "N/A"

    # Append results to the CSV
    with open(output_file, "a") as outfile:
        outfile.write(f"{temp},{line1},{line2}\n")
t1 = time.time()
print(f"All simulations completed. Results saved to '{output_file}'.")
print('time running: ',t1-t0)