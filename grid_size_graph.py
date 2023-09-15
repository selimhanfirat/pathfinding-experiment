import os
import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score

# Function to calculate the average CPU time from a list of CPU times
def calculate_average_cpu_time(cpu_time_data):
    return sum(cpu_time_data) / len(cpu_time_data)

# Define the directory containing the CSV files
ex_times_directory = "ex_times"

# Initialize lists to store data for Dijkstra and A* algorithms at different grid sizes
dijkstra_avg_cpu_time = []
a_star_avg_cpu_time = []

# Define the grid sizes you have (128, 256, 512, 1024)
grid_sizes = [128, 256, 512, 1024]

# Loop through grid sizes
for grid_size in grid_sizes:
    # Define the paths to the CSV files for Dijkstra and A* at the current grid size
    dijkstra_csv_path = os.path.join(ex_times_directory, f'Dijkstra/grid_size/{grid_size}.csv')
    a_star_csv_path = os.path.join(ex_times_directory, f'A*/grid_size/{grid_size}.csv')

    # Read the CPU time data from the CSV files
    dijkstra_cpu_time_data = []
    a_star_cpu_time_data = []

    with open(dijkstra_csv_path, 'r') as dijkstra_csv_file:
        dijkstra_reader = csv.DictReader(dijkstra_csv_file)
        for row in dijkstra_reader:
            dijkstra_cpu_time_data.append(float(row['runtime']))

    with open(a_star_csv_path, 'r') as a_star_csv_file:
        a_star_reader = csv.DictReader(a_star_csv_file)
        for row in a_star_reader:
            a_star_cpu_time_data.append(float(row['runtime']))

    # Calculate the average CPU time for Dijkstra and A* at the current grid size
    dijkstra_avg_time = calculate_average_cpu_time(dijkstra_cpu_time_data)
    a_star_avg_time = calculate_average_cpu_time(a_star_cpu_time_data)

    # Append the average times to the respective lists
    dijkstra_avg_cpu_time.append(dijkstra_avg_time)
    a_star_avg_cpu_time.append(a_star_avg_time)

# Create a line graph showing the average CPU time vs. grid size
plt.figure(figsize=(8, 6))
plt.plot(grid_sizes, dijkstra_avg_cpu_time, label='Dijkstra', marker='o')
plt.plot(grid_sizes, a_star_avg_cpu_time, label='A*', marker='o')

# Initialize variables to store best regression model information for Dijkstra and A*
best_dijkstra_regression_model = None
best_dijkstra_r_squared = -1
best_dijkstra_degree = None

best_a_star_regression_model = None
best_a_star_r_squared = -1
best_a_star_degree = None

# Test different regression models and determine the best ones for Dijkstra and A*
for degree in range(1, 4):  # Try linear, quadratic, and cubic regressions
    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(np.array(grid_sizes).reshape(-1, 1))

    # Dijkstra
    dijkstra_lin_reg = LinearRegression()
    dijkstra_lin_reg.fit(X_poly, dijkstra_avg_cpu_time)
    dijkstra_pred = dijkstra_lin_reg.predict(X_poly)
    dijkstra_r_squared = r2_score(dijkstra_avg_cpu_time, dijkstra_pred)

    # A*
    a_star_lin_reg = LinearRegression()
    a_star_lin_reg.fit(X_poly, a_star_avg_cpu_time)
    a_star_pred = a_star_lin_reg.predict(X_poly)
    a_star_r_squared = r2_score(a_star_avg_cpu_time, a_star_pred)

    print(f'Degree-{degree} Polynomial Regression (Dijkstra): R-squared = {dijkstra_r_squared:.4f}')
    print(f'Degree-{degree} Polynomial Regression (A*): R-squared = {a_star_r_squared:.4f}')

    if dijkstra_r_squared > best_dijkstra_r_squared:
        best_dijkstra_r_squared = dijkstra_r_squared
        best_dijkstra_regression_model = dijkstra_lin_reg
        best_dijkstra_degree = degree

    if a_star_r_squared > best_a_star_r_squared:
        best_a_star_r_squared = a_star_r_squared
        best_a_star_regression_model = a_star_lin_reg
        best_a_star_degree = degree

# Use the best correlated regression models to draw the best fit lines for Dijkstra and A*
x_fit = np.linspace(min(grid_sizes), max(grid_sizes), 100)
x_fit_poly = poly.transform(x_fit.reshape(-1, 1))
y_fit_dijkstra = best_dijkstra_regression_model.predict(x_fit_poly)
y_fit_a_star = best_a_star_regression_model.predict(x_fit_poly)

# Plot the best fit lines
plt.plot(x_fit, y_fit_dijkstra, linestyle='--', color='blue', label=f'Dijkstra (Degree-{best_dijkstra_degree} Poly Fit)')
plt.plot(x_fit, y_fit_a_star, linestyle='--', color='orange', label=f'A* (Degree-{best_a_star_degree} Poly Fit)')

# Add labels and title
plt.xlabel('Grid Size')
plt.ylabel('Average CPU Time (s)')
plt.title('Average CPU Time vs. Grid Size')

# Add a legend
plt.legend()



print(f'Best correlated regression model (Dijkstra): Degree-{best_dijkstra_degree} Polynomial Regression')
print(f'Best R-squared value (Dijkstra): {best_dijkstra_r_squared:.4f}')

print(f'Best correlated regression model (A*): Degree-{best_a_star_degree} Polynomial Regression')
print(f'Best R-squared value (A*): {best_a_star_r_squared:.4f}')

grid_size_to_estimate = 100

# Estimate the average CPU time for Dijkstra at the specified grid size
x_poly_estimate = poly.transform(np.array([grid_size_to_estimate]).reshape(-1, 1))
dijkstra_time_estimate = best_dijkstra_regression_model.predict(x_poly_estimate)[0]

# Estimate the average CPU time for A* at the specified grid size
a_star_time_estimate = best_a_star_regression_model.predict(x_poly_estimate)[0]

def percentage_difference(num1, num2):
    return abs(num1 - num2) / ((num1 + num2) / 2) * 100

percentage_difference_dijkstra = percentage_difference(dijkstra_time_estimate, a_star_time_estimate)
print(f'Estimated Average CPU Time for Dijkstra ({grid_size_to_estimate}x{grid_size_to_estimate}): {dijkstra_time_estimate:.4f} seconds')
print(f'Estimated Average CPU Time for A* ({grid_size_to_estimate}x{grid_size_to_estimate}): {a_star_time_estimate:.4f} seconds')
print(f'Percentage Difference (Dijkstra vs. A*): {percentage_difference_dijkstra:.2f}%')

# Show the plot
plt.grid(True)
plt.show
