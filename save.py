import csv
import os

# Function to parse memory log text and extract the second number
def parse_memory_log(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    memory_data = []
    current_section = []  # Initialize current_section here
    prev_line_number = None  # Initialize prev_line_number
    section_count = 1  # Initialize section_count

    for line in lines:
        # Check if the line starts with a number (possibly with leading spaces)
        if line.strip() and line.lstrip()[0].isdigit():
            line_number = int(line.strip().split()[0])

            # If prev_line_number is not None and the current line_number is smaller, calculate and append peak and average
            if prev_line_number is not None and line_number < prev_line_number:
                if current_section:
                    peak_memory = max(current_section)
                    avg_memory = sum(current_section) / len(current_section)
                    section_data = {'grid': section_count, 'peak': peak_memory, 'average': avg_memory}
                    memory_data.append(section_data)
                    current_section = []  # Start a new list
                    section_count += 1  # Increment section_count

            # Split the line by spaces and get the second part
            split_line = line.strip().split()
            if len(split_line) >= 2:
                try:
                    second_number = float(split_line[1])
                    current_section.append(second_number)
                except ValueError:
                    pass

            prev_line_number = line_number  # Update prev_line_number

    # Check if there is any data in the current_section and add it to memory_data
    if current_section:
        peak_memory = max(current_section)
        avg_memory = sum(current_section) / len(current_section)
        section_data = {'grid': section_count, 'peak': peak_memory, 'average': avg_memory}
        memory_data.append(section_data)

    return memory_data

def write_memory_data_to_csv(file_path, memory_data):
    with open(file_path, 'w', newline='') as csv_file:
        fieldnames = ['grid', 'peak', 'average']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the data
        for section in memory_data:
            writer.writerow(section)

logs_directory = "logs/"
results_directory = "results/"

# Loop through log files in the logs directory
for algorithm in os.listdir(logs_directory):
    algorithm_logs_dir = os.path.join(logs_directory, algorithm)
    algorithm_results_dir = os.path.join(results_directory, algorithm)

    if os.path.isdir(algorithm_logs_dir):
        for sub_directory in os.listdir(algorithm_logs_dir):
            sub_logs_dir = os.path.join(algorithm_logs_dir, sub_directory)
            sub_results_dir = os.path.join(algorithm_results_dir, sub_directory)

            if os.path.isdir(sub_logs_dir):
                # Create the corresponding results directory if it doesn't exist
                os.makedirs(sub_results_dir, exist_ok=True)

                for log_filename in os.listdir(sub_logs_dir):
                    if log_filename.endswith(".txt"):
                        log_file_path = os.path.join(sub_logs_dir, log_filename)

                        # Parse the logs
                        memory_data = parse_memory_log(log_file_path)

                        # Create the corresponding CSV file in the results directory
                        csv_filename = os.path.splitext(log_filename)[0] + ".csv"
                        csv_file_path = os.path.join(sub_results_dir, csv_filename)
                        write_memory_data_to_csv(csv_file_path, memory_data)

